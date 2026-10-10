/* FlashMed — service worker (fork do ClínicaMed).
   BUMPAR a constante CACHE a CADA deploy (fl-v1, fl-v2, …): python3 bump.py. Sem isso o app fica preso na
   versão velha e a correção vira fantasma.
   Estáticos usam stale-while-revalidate: bump de versão não basta quando a borda do CDN
   devolve conteúdo velho para o precache. HTML é network-first. */
const CACHE="fl-v8", FONTES="fl-fontes-v1", LIVROS="fl-livros-v1";
const PRE=["./assets/fonts/inter-400.ttf","./assets/fonts/inter-500.ttf","./assets/fonts/inter-600.ttf","./assets/fonts/inter-700.ttf","./","./index.html","./taxonomia.js?v=8","./provas.js?v=8","./banco.js?v=8","./exames.js?v=8","./flash.js?v=8",
           "./leituras.js?v=8","./mtsync.js?v=8","./migra.js?v=8","./nuvem.js?v=8","./mtfiltro.js?v=8","./mtsinal.js?v=8","./mterrata.js?v=8","./indice-leituras.js?v=8","./manifest.webmanifest",
           "./leituras/_leitura.css?v=8","./leituras/_leitura.js?v=8"];
/* SDK da conta (Firebase 10.13.2), vendorizado. Fica no balde FONTES, que sobrevive ao bump:
   sem ele o app não abre offline depois de um deploy, e baixar 515 KB a cada versão é
   desperdício. Sem "./" de propósito: o bump.py não versiona, e o mtsync pede estes caminhos. */
const VENDOR=["vendor/firebase-app-compat.js","vendor/firebase-auth-compat.js","vendor/firebase-firestore-compat.js"];
/* As figuras (leituras/fig/*.svg) NÃO entram no precache — são 41 arquivos e 291 KB, e nem toda
   leitura usa todas. Elas caem no cache pela regra geral de estáticos (stale-while-revalidate)
   na primeira vez que a leitura abre online, e a partir daí funcionam offline. */
self.addEventListener("install",e=>{
  e.waitUntil(Promise.all([
    caches.open(CACHE).then(c=>Promise.allSettled(PRE.map(u=>c.add(u)))),
    caches.open(FONTES).then(c=>Promise.allSettled(VENDOR.map(u=>c.match(u).then(h=>h||c.add(u)))))
  ]).then(()=>self.skipWaiting()));
});
self.addEventListener("activate",e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(
    ks.filter(k=>k!==CACHE&&k!==FONTES&&k!==LIVROS).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",e=>{
  const req=e.request; if(req.method!=="GET")return;
  const url=new URL(req.url);
  /* SÓ fontes e os módulos versionados do Firebase entram no cache-first. O teste antigo era
     hostname.endsWith("googleapis.com"), que engolia firestore.googleapis.com — o canal de
     escuta do Firestore usa GET, e servir isso da cache trava a sincronização em silêncio. */
  /* cdn.jsdelivr.net (ícones Tabler) fica no balde de fontes, que sobrevive ao bump de
     versão, mas em stale-while-revalidate: o caminho tem versão maior (@3) e pode andar.
     O mermaid saiu daqui: agora é vendor/mermaid-<versão exata>/ (ver abaixo). */
  if(url.hostname==="cdn.jsdelivr.net"){
    e.respondWith(caches.open(FONTES).then(async c=>{
      const hit=await c.match(req);
      const rede=fetch(req).then(r=>{if(r.ok)c.put(req,r.clone());return r}).catch(()=>null);
      return hit||(await rede)||Response.error();
    })); return;
  }
  if(url.hostname==="fonts.googleapis.com"||url.hostname==="fonts.gstatic.com"||
     (url.hostname==="www.gstatic.com"&&url.pathname.startsWith("/firebasejs/"))){
    e.respondWith(caches.open(FONTES).then(async c=>{
      const hit=await c.match(req); if(hit)return hit;
      try{const r=await fetch(req);if(r.ok)c.put(req,r.clone());return r}catch(err){return hit||Response.error()}
    })); return;
  }
  if(url.origin!==location.origin)return;
  /* vendor/: Firebase e mermaid (3,5 MB), com a versão no caminho. Cache-first no balde que
     sobrevive ao bump, para não re-baixar a cada deploy. Trocar de versão = trocar o caminho. */
  if(url.pathname.includes("/vendor/")){
    e.respondWith(caches.open(FONTES).then(async c=>{
      const hit=await c.match(req,{ignoreSearch:true}); if(hit)return hit;
      const r=await fetch(req); if(r.ok)c.put(req,r.clone()); return r;
    })); return;
  }
  /* HTML é network-first, mas AGORA GUARDA o que baixou. Antes não guardava: o app abria offline
     e as 97 leituras não — a leitura caía no fallback e servia o index.html DENTRO do iframe, que
     é o app inteiro dentro da leitura. O fallback usa caches.match global de propósito, para achar
     também o que o botão "guardar no aparelho" pôs no balde LIVROS. */
  if(req.mode==="navigate"||req.destination==="document"){
    const leitura=url.pathname.includes("/leituras/");
    e.respondWith(
      fetch(req).then(r=>{
        if(r.ok&&r.type==="basic")caches.open(leitura?LIVROS:CACHE).then(c=>c.put(req,r.clone())).catch(()=>{});
        return r;
      }).catch(()=>caches.match(req).then(r=>r||caches.match("./index.html"))));
    return;
  }
  /* As figuras vão para o balde da biblioteca, que sobrevive ao bump — um ECG não muda de deploy
     para deploy, e re-baixar 291 KB de SVG a cada versão é desperdício em rede de hospital. */
  const balde=/\/leituras\/(.+\/)?fig\//.test(url.pathname)?LIVROS:CACHE;
  e.respondWith(caches.open(balde).then(async c=>{
    const hit=await c.match(req);
    const rede=fetch(req).then(r=>{if(r.ok)c.put(req,r.clone());return r}).catch(()=>null);
    return hit||(await rede)||(await caches.match(req))||Response.error();
  }));
});
