/* ================================================================
   FlashMed — conta MedTech e sincronização (fork do nuvem.js do ClínicaMed, 07/10/2026).

   O app na nuvem continua sendo "flashmed" (users/{uid}/apps/flashmed/sync), o mesmo do FlashMed
   antigo (flashmed.html, até 06/10/2026): é o id que o acesso por produto e a caixa de sinalizações
   conhecem. Para não misturar formatos, as coleções novas têm prefixo "f2" (o antigo gravava "resp"
   como mapa {sel,ok}; aqui "resp" é histórico). O progresso antigo entra UMA vez por conta em
   legado(): cada resposta do FlashMed antigo vira uma entrada no histórico da mesma questão aqui,
   pelo mapa migra.js (id antigo "prova:índice" → chave por conteúdo).

   Todo o trabalho pesado está no mtsync.js (cópia de ~/Documents/Claude/_mtsync/, testado
   por `node _mtsync/teste.js`): portão de login, um documento por item na nuvem, fila
   offline do próprio Firestore e recebimento em tempo real. Aqui ficam só as coisas do
   FlashMed:
     - quais chaves sincronizam e de que tipo são;
     - o resumo agregado (users/{uid}/apps/flashmed_resumo), no mesmo formato do ClínicaMed;
     - a migração, uma vez por conta, do FlashMed antigo;
     - o chip do cabeçalho e o bloco "Conta" de Ajustes.

   Pedido do Matheus (25/09): o app só abre logado, a sincronização é automática e o
   cliente nunca precisa fazer backup. Por isso não há mais exportar/importar/restaurar.

   NÃO sincronizam (são a tela deste aparelho): cfg (aba, tema, filtros), pos, simativo.
   erros é derivado de resp: é recalculado quando chegam respostas de outro aparelho.
   ================================================================ */
const NUVEM=(function(){

/* chave local (ST, localStorage) → nome da coleção na nuvem */
const LOCAL_NUVEM={resp:"f2resp",fav:"f2fav",flash:"f2flash",sinal:"f2sinal",lidas:"f2lidas",prog:"f2prog",atividade:"f2atividade",sim:"f2sim",contest:"f2contest"};
const NUVEM_LOCAL=Object.fromEntries(Object.entries(LOCAL_NUVEM).map(([a,b])=>[b,a]));
const COLECOES={
  f2resp:{tipo:"hist",teto:60},
  f2fav:{tipo:"mapa"}, f2flash:{tipo:"mapa"}, f2sinal:{tipo:"mapa"}, f2lidas:{tipo:"mapa"}, f2prog:{tipo:"mapa"},
  f2atividade:{tipo:"soma"},
  f2sim:{tipo:"lista",id:"quando",ordena:(a,b)=>String(a.quando).localeCompare(String(b.quando))},
  f2contest:{tipo:"lista",id:"quando",teto:60,ordena:(a,b)=>String(b.quando).localeCompare(String(a.quando))}
};

let coord=null, ultimoResumo="", resumoT=null;

/* ---------- erros derivados de resp (mesma regra do registraResposta) ---------- */
function derivaErros(resp){
  const out=[];
  Object.keys(resp||{}).forEach(ch=>{
    const h=((resp[ch]||{}).hist)||[];
    if(!h.some(r=>!r.ok))return;
    let n=0; for(let i=h.length-1;i>=0;i--){if(h[i].ok)n++;else break}
    if(n<2)out.push(ch);
  });
  return out;
}

/* ---------- resumo para a coordenação ----------------------------------
   Calculado no aparelho (só aqui a chave da resposta vira área do edital) e publicado num
   doc pequeno e separado. A coordenação lê esse doc, nunca o caderno de respostas. */
function resumo(){
  const resp=ST.resp||{}, porArea={};
  let tentativas=0, unicas=0, acertos=0;
  Object.keys(resp).forEach(ch=>{
    const h=((resp[ch]||{}).hist)||[]; if(!h.length)return;
    unicas++; tentativas+=h.length;
    const certa=!!h[h.length-1].ok; if(certa)acertos++;
    const q=(typeof QIDX!=="undefined")&&QIDX.get(ch); if(!q)return;
    const a=porArea[q.tema]||(porArea[q.tema]={n:0,ok:0}); a.n++; if(certa)a.ok++;
  });
  const dias=Object.keys(ST.atividade||{}).sort();
  const corte=new Date(Date.now()-7*864e5).toISOString().slice(0,10);
  const ultimos7=dias.filter(d=>d>corte).reduce((s,d)=>s+(+ST.atividade[d]||0),0);
  const sims=Array.isArray(ST.sim)?ST.sim:[];
  return {respondidas:tentativas, unicas, acertos,
    leituras:Object.keys(ST.lidas||{}).length, cartoes:Object.keys(ST.flash||{}).length,
    simulados:sims.length,
    notaMedia:sims.length?Math.round(sims.reduce((s,x)=>s+(+x.nota||0),0)/sims.length*100)/100:0,
    diasAtivos:dias.length, ultimos7, ultimaAtividade:dias[dias.length-1]||"",
    porArea, versao:(typeof V!=="undefined")?V:""};
}
function agendaResumo(){ clearTimeout(resumoT); resumoT=setTimeout(publicaResumo,4000) }
async function publicaResumo(){
  const u=MTS.usuario; if(!u||!MTS.db)return;
  const r=resumo(), s=JSON.stringify(r);
  if(s===ultimoResumo)return;
  try{
    await MTS.db.collection("users").doc(u.uid).collection("apps").doc("flashmed_resumo")
      .set({json:s, atualizadoEm:new Date().toISOString(), nome:u.displayName||"", email:u.email||""},{merge:true});
    ultimoResumo=s;
  }catch(e){ console.warn("nuvem: resumo não publicado",e) }
}
/* A pessoa tem de PODER SABER que é acompanhada: a coordenação grava este doc na área dela. */
async function leCoord(){
  const u=MTS.usuario; if(!u||!MTS.db){coord=null;return}
  try{ const s=await MTS.db.collection("users").doc(u.uid).collection("apps").doc("flashmed_coord").get();
    coord=s.exists?s.data():null;
  }catch(e){ coord=null }
}

/* ---------- migração do FlashMed antigo (uma vez por conta) ----------
   O FlashMed até 06/10/2026 gravava cada resposta como um doc do tipo mapa em
   users/{uid}/apps/flashmed/sync com c:"resp", i:"<prova>:<índice>", j:'{"sel":2,"ok":true,"t":...}'.
   Aqui ela vira uma entrada no histórico da mesma questão (achada pelo mapa window.MIGRA). A
   alternativa marcada continua certa: as questões de prova estão com as alternativas na ordem
   oficial nos dois apps. Nada é apagado do formato antigo. */
async function legado(ctx){
  const MG=window.MIGRA||{}; if(!Object.keys(MG).length)return true;
  const col=ctx.db.collection("users").doc(ctx.uid).collection("apps").doc("flashmed").collection("sync");
  const snap=await Promise.race([col.where("c","==","resp").get({source:"server"}),new Promise((_,f)=>setTimeout(()=>f(new Error("tempo")),12000))]);
  let n=0;
  snap.forEach(doc=>{
    const d=doc.data()||{}; if(d.del)return;
    const ch=MG[d.i]; if(!ch)return;
    let v; try{v=typeof d.j==="string"?JSON.parse(d.j):d.v}catch(e){return}
    if(!v||typeof v.sel!=="number"||v.sel<0)return;
    const ts=+v.t||Date.now(), r=ST.resp[ch]||(ST.resp[ch]={hist:[]});
    if(r.hist.some(h=>h.ts===ts))return;
    r.hist.push({d:new Date(ts).toISOString().slice(0,10),ok:!!v.ok,alt:v.sel,m:"flashmed-antigo",ts});
    r.hist.sort((a,b)=>a.ts-b.ts); n++;
  });
  if(n){ARM.save(PREF+"resp",ST.resp);const er=derivaErros(ST.resp);ST.erros=er;ARM.save(PREF+"erros",er);
    setTimeout(()=>{MTS.mudou("f2resp");try{UI.banner("ok",`${n} respostas do FlashMed antigo foram trazidas para o seu histórico.`)}catch(e){}},1500)}
  return true;
}

/* ---------- apagar o que é da conta que saiu ---------- */
async function limparLocal(){
  try{Object.keys(localStorage).filter(k=>k.startsWith(PREF)&&k!==PREF+"tema").forEach(k=>localStorage.removeItem(k))}catch(e){}
  try{localStorage.removeItem("msn_fila:flashmed")}catch(e){}   /* fila das sinalizações: não pode sair com o login da conta nova */
  try{if(ARM.db)ARM.db.close()}catch(e){}
  await new Promise(r=>{try{const q=indexedDB.deleteDatabase("fl-db");q.onsuccess=q.onerror=q.onblocked=()=>r()}catch(e){r()}});
}

/* ---------- chegou algo de outro aparelho ---------- */
function aoReceber(colsN){
  const cols=colsN.map(c=>NUVEM_LOCAL[c]||c);
  if(cols.includes("resp")){const er=derivaErros(ST.resp);ST.erros=er;ARM.save(PREF+"erros",er)}
  /* repinta só telas de consulta: redesenhar a questão aberta tiraria a pessoa do lugar */
  const aba=(ST.cfg||{}).aba;
  if(["inicio","painel","ajustes","leituras","cartoes"].includes(aba)&&typeof PINTA!=="undefined"&&PINTA[aba])PINTA[aba]();
  /* bandeira da questão aberta acompanha o outro aparelho sem redesenhar a questão */
  if(cols.includes("sinal")&&typeof SINAL!=="undefined"&&ST.pos&&ST.pos.chq)SINAL.repinta(ST.pos.chq);
  agendaResumo();
}

/* ---------- chip do cabeçalho ---------- */
function pintaChip(){
  const b=document.getElementById("btConta"); if(!b)return;
  const u=MTS.usuario; if(!u){b.hidden=true;return}
  b.hidden=false; b.classList.add("logado");
  const s=MTS._sit, d=MTS.descreve(s);
  const ico=d.cl==="erro"?"cloud-exclamation":d.cl==="pend"?(s.online?"cloud-upload":"cloud-off"):"cloud-check";
  const nome=(u.displayName||u.email||"conta").split(/[ @]/)[0];
  b.innerHTML=`<i class="ti ti-${ico}" aria-hidden="true"></i><span>${nome.replace(/[<>&]/g,"")}</span>`;
  b.title=d.txt;
  const m=document.getElementById("btLinha"); if(m)m.hidden=true;
}

function contaMarkup(){
  const u=MTS.usuario; if(!u)return `<p class="mini">Abrindo sua conta…</p>`;
  const d=MTS.descreve();
  const cor=d.cl==="erro"?"var(--erro,#b42318)":d.cl==="pend"?"var(--ink2)":"var(--brandInk)";
  return `<p class="mini">Conectado como <b>${esc(u.displayName||u.email||"")}</b>${u.displayName&&u.email?` (${esc(u.email)})`:""}.</p>
   <p class="mini" id="ctSit" style="margin-top:6px;color:${cor}">${esc(d.txt)}</p>
   <p class="mini" style="margin-top:6px">Tudo o que você faz é salvo sozinho na sua conta enquanto estuda, e aparece igual no celular e no computador. Sem internet, o app continua funcionando e envia depois.</p>
   ${coord?`<p class="mini" style="margin-top:6px;padding:8px 10px;background:var(--aviSup);border-radius:8px">
     <b>A coordenação acompanha seu desempenho neste app.</b> ${esc(coord.coordenador||"")}
     ${coord.turma?`incluiu você na turma ${esc(coord.turma)}`:"incluiu você na turma"} e vê o resumo do seu estudo:
     quantas questões você fez, o acerto por área, leituras concluídas, simulados e há quanto tempo você não entra.
     O que você respondeu em cada questão <b>não</b> aparece para ninguém.</p>`:""}
   <div class="linha" style="margin-top:10px"><button class="bt sec" id="btSair">Sair da conta</button>
    <a class="bt sec" href="/provas.html">MedTech Provas</a></div>`;
}

/* ---------- boot ---------- */
function boot(){
  MTS.aoMudarSituacao(s=>{
    pintaChip();
    const el=document.getElementById("ctSit"); if(el){const d=MTS.descreve(s);el.textContent=d.txt}
    if(!s.pendentes&&!s.enviando)agendaResumo();
  });
  MTS.iniciar({
    app:"flashmed", nome:"FlashMed", pref:PREF, vendor:"vendor/",
    cores:(()=>{const c=getComputedStyle(document.documentElement);const g=k=>c.getPropertyValue(k).trim();
      return {cor:g("--c-marca")||"#C2410C",sobrecor:g("--brandTxt")||"#fff",fundo:g("--papel")||"#fff",texto:g("--ink")||"#1d2433",suave:g("--ink2")||"#5b6475",borda:g("--linhaF")||"#d5d9e0",campo:g("--papel")||"#fff"}})(),
    colecoes:COLECOES,
    ler:c=>ST[NUVEM_LOCAL[c]],
    gravar:(c,v)=>{const k=NUVEM_LOCAL[c];ST[k]=v;ARM.save(PREF+k,v)},
    aoReceber,
    legado,
    limparLocal,
    aoEntrar(u){
      leCoord().then(()=>{if((ST.cfg||{}).aba==="ajustes")pintaAjustes()});
      pintaChip();
      if((ST.cfg||{}).aba==="ajustes")pintaAjustes();
    }
  });
}
return {boot, mudou:k=>{const c=LOCAL_NUVEM[k];if(c)MTS.mudou(c)}, resumo, pintaChip, contaMarkup,
  get usuario(){return MTS.usuario}, get coord(){return coord},
  sair(){MTS.sair()}};
})();
