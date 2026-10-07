/* Comportamentos compartilhados das leituras.
   - tema: vem por ?tema= na abertura e por postMessage quando o app troca com a leitura aberta;
   - progresso: avisa o app (iframe pai) até onde a pessoa rolou, para o "continuar lendo" e
     para marcar como lida sozinha ao chegar ao fim;
   - fluxogramas: carrega o mermaid só se a página tiver algum, com as cores do tema; offline
     sem cache, o texto do diagrama continua legível (é isso que o <pre> mostra). */
(function(){
  /* FlashMed: as leituras importadas ficam em subpastas (leituras/cm/, leituras/cir/). Caminhos
     do mermaid e o nome do arquivo saem da URL deste script, não do documento. */
  var BASE=(document.currentScript&&document.currentScript.src)||location.href;
  function aplica(t){ if(t==="escuro"||t==="claro")document.documentElement.setAttribute("data-tema",t) }
  var p=new URLSearchParams(location.search); aplica(p.get("tema"));
  /* Embutida no app, o sumário vive na coluna lateral — mantê-lo aqui repetiria meia tela de
     links na abertura, que era o que empurrava o texto para baixo. Fora do app (leitura aberta
     direto pelo endereço) ele continua no lugar. */
  /* `embutida=1` só marca que estamos dentro do app; quem manda esconder o sumário é a mensagem
     `sumario`, porque depende da largura da janela do app, não da nossa. */
  if(p.get("embutida")==="1") document.documentElement.classList.add("noApp");
  addEventListener("message",function(e){
    if(!e.data)return;
    if(e.data.cm==="tema"){aplica(e.data.tema);desenha(true)}
    if(e.data.cm==="ir"){ var el=document.getElementById(e.data.id);
      /* salto direto: com 14 mil pixels de texto, a rolagem suave leva segundos e qualquer
         toque no meio do caminho a cancela — o sumário deixaria de funcionar sem avisar. */
      if(el)el.scrollIntoView({behavior:"auto",block:"start"}) }
    if(e.data.cm==="sumario"){ document.documentElement.classList.toggle("embutida", !!e.data.lateral) }
  });

  var arq=(function(){var p=decodeURIComponent(location.pathname),i=p.lastIndexOf("/leituras/");return i>=0?p.slice(i+10):p.split("/").pop()})();
  /* Só há progresso se a página for maior que a janela. No instante do load, antes de fonte
     e layout assentarem, scrollHeight pode ser igual a clientHeight — reportar 100% aí marcaria
     toda leitura como lida ao abrir. Por isso: max pequeno devolve 0, e o primeiro aviso só
     sai com rolagem de verdade, nunca no load. */
  function pct(){var h=document.documentElement,max=h.scrollHeight-h.clientHeight;
    return max<200?0:Math.round(100*h.scrollTop/max)}
  var barra,ultimo=-1,tm;
  function progresso(){
    if(!barra){barra=document.createElement("div");barra.id="barraLeitura";document.body.appendChild(barra)}
    var v=pct(); barra.style.width=v+"%";
    if(v===ultimo)return; ultimo=v;
    clearTimeout(tm); tm=setTimeout(function(){
      try{ if(parent&&parent!==window)parent.postMessage({cm:"prog",f:arq,pct:v},"*") }catch(e){}
    },400);
  }
  /* diz ao app qual capítulo está na tela, para o sumário lateral acompanhar a leitura */
  var secAtual=null;
  function secaoVisivel(){
    var hs=document.querySelectorAll("h2[id],h3[id]"), achou=null;
    for(var i=0;i<hs.length;i++){ if(hs[i].getBoundingClientRect().top<=140) achou=hs[i].id; else break }
    if(achou&&achou!==secAtual){ secAtual=achou;
      try{ if(parent&&parent!==window)parent.postMessage({cm:"sec",f:arq,id:achou},"*") }catch(e){} }
  }
  addEventListener("scroll",function(){progresso();secaoVisivel()},{passive:true});
  addEventListener("load",function(){
    /* link copiável em cada seção */
    document.querySelectorAll("h2[id]").forEach(function(h){
      var a=document.createElement("a");a.className="lnk";a.href="#"+h.id;a.title="copiar link desta seção";a.textContent="#";
      a.onclick=function(ev){ev.preventDefault();history.replaceState(null,"","#"+h.id);
        try{navigator.clipboard.writeText(location.href)}catch(e){}};
      h.appendChild(a);
    });
    if(location.hash){var el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el)el.scrollIntoView()}
  });

  /* Tabelas de várias colunas mantêm uma largura de leitura útil no celular. */
  function preparaTabelas(){
    document.querySelectorAll("table").forEach(function(t){
      var larga=Array.from(t.rows).some(function(r){return r.cells.length>=3});
      if(!larga)return;
      t.classList.add("tabelaLarga");
      var caixa=t.parentElement;
      if(!caixa.classList.contains("rolagem")){
        caixa=document.createElement("div");caixa.className="rolagem";
        t.parentNode.insertBefore(caixa,t);caixa.appendChild(t);
      }
      caixa.tabIndex=0;caixa.setAttribute("role","region");
      caixa.setAttribute("aria-label","Tabela com rolagem horizontal");
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",preparaTabelas);else preparaTabelas();

  /* ---- mermaid ---- */
  var carregando=false, pronto=false;
  function escuro(){return document.documentElement.getAttribute("data-tema")==="escuro"||
    (document.documentElement.getAttribute("data-tema")!=="claro"&&matchMedia("(prefers-color-scheme:dark)").matches)}
  function tema(){var d=escuro();return {theme:"base",themeVariables:{
    fontFamily:"Figtree,system-ui,sans-serif",fontSize:"14px",
    primaryColor:d?"#14292B":"#E3F1F1",primaryTextColor:d?"#E9EBEE":"#23272E",primaryBorderColor:d?"#4FB8BD":"#0B6A72",
    lineColor:d?"#A3A9B2":"#5E646B",secondaryColor:d?"#23272E":"#F1F1EC",tertiaryColor:d?"#1B1E23":"#FFFFFF",
    background:d?"#1B1E23":"#FFFFFF",mainBkg:d?"#14292B":"#E3F1F1",nodeBorder:d?"#4FB8BD":"#0B6A72",
    clusterBkg:d?"#1B1E23":"#FAFAF8",clusterBorder:d?"#363C44":"#DDDDD5",edgeLabelBackground:d?"#1B1E23":"#FFFFFF",
    titleColor:d?"#E9EBEE":"#23272E"}}}
  var fontes={};   /* texto original de cada diagrama, para redesenhar ao trocar o tema */
  function desenha(redesenhar){
    var pres=document.querySelectorAll("pre.mermaid"); if(!pres.length)return;
    if(!window.mermaid){
      if(carregando)return; carregando=true;
      var s=document.createElement("script");s.src=new URL("../vendor/mermaid-11.17.2/mermaid.min.js",BASE).href; /* versão exata servida daqui (antes: @11 móvel no jsDelivr, sem SRI) */
      s.onload=function(){pronto=true;desenha()};
      s.onerror=function(){pres.forEach(function(p){var n=document.createElement("div");n.className="off";
        n.textContent="Fluxograma em texto: sem conexão para desenhar agora.";p.parentNode.insertBefore(n,p)})};
      document.head.appendChild(s); return;
    }
    pres.forEach(function(p,i){ if(!fontes[i])fontes[i]=p.textContent; if(redesenhar){p.removeAttribute("data-processed");p.innerHTML="";p.textContent=fontes[i]} });
    mermaid.initialize(Object.assign({startOnLoad:false,securityLevel:"strict",flowchart:{curve:"basis",htmlLabels:true,padding:8}},tema()));
    mermaid.run({nodes:pres}).catch(function(e){console.warn("mermaid",e)});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){desenha()});else desenha();

  /* ---- ampliar figura e fluxograma (23/09/2026) ----
     Na coluna de 664 px, 16 dos 38 fluxogramas saíam com letra efetiva abaixo de 11 px (um deles com
     4,7 px) e os ECGs de 12 derivações ficam miúdos no celular. Tocar abre a peça no quadro inteiro,
     no tamanho em que a letra se lê (fluxograma: largura natural do desenho; ECG: pelo menos 1100 px),
     com rolagem para os lados, + e − para ampliar, Esc ou X para fechar. */
  var AMP=null;
  function txtDe(el){return (el.innerText||el.textContent).replace(/\s+/g," ").trim()}
  function fechaAmp(){ if(AMP){AMP.remove();AMP=null;document.documentElement.classList.remove("ampliando")} }
  function abreAmp(peca,legenda,larguraBase){
    fechaAmp();
    var ov=document.createElement("div");ov.className="amp";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");
    ov.innerHTML='<div class="ampBarra"><span class="ampLeg"></span><button type="button" data-z="-1" aria-label="Diminuir">−</button><button type="button" data-z="1" aria-label="Ampliar">+</button><button type="button" data-z="0" aria-label="Fechar">×</button></div><div class="ampArea"><div class="ampPeca"></div></div>';
    ov.querySelector(".ampLeg").textContent=legenda||"";
    var caixa=ov.querySelector(".ampPeca"); caixa.appendChild(peca);
    var area=ov.querySelector(".ampArea");
    var cabe=Math.max(280,innerWidth-32), w=Math.max(cabe,larguraBase||cabe);
    function aplicaW(){ caixa.style.width=Math.round(w)+"px" }
    aplicaW();
    ov.addEventListener("click",function(e){
      var b=e.target.closest("button");
      if(b){var z=+b.dataset.z; if(!z){fechaAmp();return}
        var cx=(area.scrollLeft+area.clientWidth/2)/area.scrollWidth, cy=(area.scrollTop+area.clientHeight/2)/area.scrollHeight;
        w=Math.min(4000,Math.max(cabe*0.6,w*(z>0?1.35:1/1.35))); aplicaW();
        area.scrollLeft=cx*area.scrollWidth-area.clientWidth/2; area.scrollTop=cy*area.scrollHeight-area.clientHeight/2; return}
      if(e.target===area||e.target===ov)fechaAmp();
    });
    document.body.appendChild(ov); AMP=ov; document.documentElement.classList.add("ampliando");
    ov.querySelector('[data-z="0"]').focus({preventScroll:true});
  }
  addEventListener("keydown",function(e){ if(e.key==="Escape")fechaAmp() });
  document.addEventListener("click",function(e){
    if(AMP)return;
    var fig=e.target.closest(".fig"), fl=e.target.closest(".fluxo");
    if(fig){ var im=fig.querySelector("img"); if(!im)return;
      var leg=fig.querySelector("figcaption"), c=im.cloneNode(); c.removeAttribute("width");c.removeAttribute("height");
      var ecg=fig.classList.contains("ecg")||/\/(real-|ecg-|tira-)/.test(im.getAttribute("src")||"");
      abreAmp(c,leg?txtDe(leg):"",ecg?1100:Math.min(1400,(im.naturalWidth||600)*1.6)); return }
    if(fl){ var sv=fl.querySelector("pre.mermaid svg"); if(!sv)return;
      var vb=sv.viewBox&&sv.viewBox.baseVal, c2=sv.cloneNode(true);
      c2.removeAttribute("style");c2.setAttribute("width","100%");c2.removeAttribute("height");
      var lg=fl.querySelector(".leg"); abreAmp(c2,lg?txtDe(lg):"",vb&&vb.width?vb.width*1.05:0) }
  });
})();
