# FlashMed — preparatório ENARE / ENAMED

Reconstruído em 07/10/2026 a pedido do Matheus: "Vamos usar o FLASHMED como aplicativo preparatório para o
ENARE / ENAMED. Junte questões de todos nossos apps de questões (clínica médica, radiologia, cirurgia) e crie
questões de outras áreas como saúde mental, GO, MFC, SUS etc. Deixe o layout conforme o do ClínicaMed, só que
com cores diferentes." É um **fork do ClínicaMed** (`~/Documents/Claude/clinicamed/`): mesma arquitetura,
camada viva, motor de conta (mtsync), defesas e armadilhas. **Leia o CLAUDE.md do ClínicaMed** para o que é
comum (chave por conteúdo, Fisher-Yates, viés de tamanho, `bump.py`, `.nojekyll`, `servir.py` com charset,
escrita sem cara de IA, formato das leituras). Aqui fica só o que é PRÓPRIO do FlashMed.

Repo `MedTechBR/flashmed` (público), no ar em **medtechbr.com.br/flashmed/**. O antigo
`medtechbr.com.br/flashmed.html` (clone do quiz de farmácia, até 06/10/2026) virou redirecionamento para cá.

## A prova (conferido em 07/10/2026)
- **ENAMED** (INEP): 100 questões objetivas de 4 alternativas, 5 h, **20 por área**: Clínica Médica, Cirurgia,
  GO, Pediatria e Medicina de Família e Comunidade; Saúde Mental e Saúde Coletiva são TRANSVERSAIS. Nota por TRI.
- Desde o ENARE 2025/2026, a prova objetiva do **ENARE de acesso direto É o ENAMED**. ENAMED 2025 = 19/10/2025;
  ENAMED 2026 / ENARE 2026/27 = 13/09/2026 (gabarito definitivo do caderno 2026.2 ainda não publicado em 07/10).
- Revalida 2025.2 tem questões em comum com o ENAMED 2025 (nota_gabarito_enamed_revalida_2025).

## Taxonomia (`taxonomia.js`)
Duas camadas: `GRANDES` (clinica, cirurgia, go, ped, mfc, coletiva, mental, imagem) e `TAXONOMIA` (51
subáreas; `q.tema` = id da subárea; `t.grande` liga à grande área). Os ids de Clínica são os do ClínicaMed;
os de Cirurgia são o mapa de `importa.py` (MAPA_CIR) sobre os do CirurgiaMed. Radiologia (`imagem`) é
aprofundamento: peso 0, fora dos simulados no formato da prova. `peso` = incidência estimada numa prova de 100;
o Desempenho mostra a incidência REAL (contagem das questões de prova de acesso direto do banco).
Cenários: amb, enf, emg, uti, cc. Competências: dx, tto, urg, prev, bas.

## De onde vem cada questão (o banco é MONTADO, nunca editado à mão)
- `leva001-imp-clinicamed.json`, `leva002-imp-cirurgiamed.json`, `leva003-imp-radiologia.json`: gerados por
  **`python3 importa.py`** a partir dos `banco.js` dos outros apps (a fonte da verdade continua lá: corrigir no
  app de origem e reimportar). SUS e psiquiatria do ClínicaMed são reclassificados por `docs/reclass.json`
  (classificação feita uma vez) e, para questão nova, pela heurística `heur_sus/heur_psiq`. Do RadioTítulo
  entram SÓ as autorais sem imagem (repo privado; provas do CBR não são caderno público; imagens com licença NC).
- `leva2NN-reais-NN.json`: questões de **prova real** que os outros apps não usavam (GO, pediatria, preventiva,
  MFC, mental, e clínica/cirurgia que sobraram), extraídas verbatim dos cadernos oficiais (candidatas do
  ClínicaMed + provas do FlashMed antigo), triadas e comentadas por redatores com `docs/BRIEF_REAIS_FM.md`.
  Relatórios de cada lote (descartes e gabaritos discutíveis) em `docs/relatorios/`.
- `leva3NN-<slug>.json`: **autorais** novas (Saúde Mental, MFC, SUS, GO, Pediatria, Cirurgia, Radiologia do
  generalista) por `docs/BRIEF_AUTORAIS_FM.md` + adendo `BRIEF_AUTORAIS_FM2.md` (rodada 2: não repetir o banco,
  correta mais longa em 18 a 26%).
- `provas-extras/*.json`: provas extraídas AQUI (USP 2025 AD, ENAMED 2025, ENARE pré-requisito de Pediatria, GO,
  MFC e Psiquiatria 2024/25 e 2025/26), com fonte e método em `provas-extras/FONTES.md`. Viram levas 219-235 pela
  triagem `docs/BRIEF_REAIS_FM.md` + `BRIEF_REAIS_FM2.md` (Clínica Médica dessas provas foi descartada, menos no ENAMED).
- **Questão em duas provas** (ENAMED 2025 = Revalida 2025.2 nas questões 1 a 50): `fonte.ex` é a principal e
  `fonte.tb = [{ex, n}]` as outras. `importa.py` registra provas-extras PRIMEIRO; `monta_banco.py` agrupa as duas
  em exames.js; no app, `naProva(q,id)`/`numNaProva` e o rótulo "(também ...)".
- `monta_banco.py` concatena, tira duplicatas por chave (a primeira leva vence), **normaliza `fonte`** pela
  tabela `docs/exames.py` + `docs/ordem.json` (cada questão de prova ganha `{banca, ano, prova, ex, n}`), gera
  `exames.js` (provas na íntegra) e `migra.js` (FlashMed antigo → chave nova) e roda `valida_banco.py`.

Ordem de build: `python3 importa.py && python3 importa_leituras.py && python3 monta_banco.py && python3 gera_indice.py && python3 valida_leituras.py && python3 valida_html.py && python3 bump.py`

## Leituras
`importa_leituras.py` copia as leituras do ClínicaMed para `leituras/cm/` e as do CirurgiaMed para
`leituras/cir/` (cada uma com a sua `fig/`; só o caminho do `_leitura.css/js` e o link "treinar questões"
mudam) e monta `leituras.js` (GERADO) juntando as próprias do FlashMed (raiz de `leituras/`, índice em
`leituras/_entradas_*.json`, brief `docs/BRIEF_LEITURAS_FM.md` + adendo `BRIEF_LEITURAS_FM2.md`). Desde a rodada 2
há leituras próprias de Cirurgia (grupo "Cirurgia", primeiro na lista). `_leitura.js` foi adaptado: o nome do arquivo
é o caminho depois de `/leituras/` (ex.: `cm/asma.html`) e o mermaid é resolvido pela URL do próprio script.
O iframe codifica cada segmento do caminho (encodeURIComponent no caminho inteiro trocava `/` por `%2F` e
quebrava os relativos). `gera_indice.py` varre subpastas; `FIGS` traz caminhos relativos a `leituras/`.

## O que mudou em relação ao ClínicaMed
- Identidade: marca **#C2410C** (âmbar queimado, a cor da linha MedTech Provas), papel quente #F7F5F0, ícone de
  raio (`gera_icones.py`). Cor por aba: Início marca, Questões verde, Simulado rosa, Leituras azul, Cartões
  âmbar, Desempenho violeta. A cor de uma subárea é a da grande área dela (`corArea`).
- Prefixo local `fl_`, caches `fl-vN`/`fl-fontes-v1`/`fl-livros-v1`, IndexedDB `fl-db`.
- **Conta:** app `flashmed` no mtsync (o mesmo id do FlashMed antigo, que o acesso por produto e a caixa de
  sinalizações conhecem), com coleções prefixadas `f2` (`nuvem.js`: LOCAL_NUVEM). O antigo gravava `resp` como
  mapa {sel,ok}; o `legado()` traz essas respostas UMA vez por conta para o histórico novo via `migra.js`.
- Sem abas Prática e Turma (ENARE/ENAMED não têm prova prática; a coordenação é do ClínicaMed).
- Questões: chips de grande área + seletor de subárea + filtro por prova (`f.gr`, `f.ex`).
- Simulado: ENAMED/ENARE (100 q, 5 h, cotas `COTA_ENAMED`), por grande área (30 q), treino curto,
  "só questões de prova real", e **provas na íntegra** (`iniciaExame`: questões da edição na ordem do caderno,
  3 min por questão). Nota = percentual (o ENAMED usa TRI; não fingir nota oficial).
- Desempenho: por grande área, por subárea, **incidência nas provas reais**, cenário × competência.
- Ajustes: data da prova (contagem no Início). `?busca=<termo>` abre a busca (link do CondutAI).

## Teste local
Copiar o app para o scratchpad, injetar `~/Documents/Claude/_mtsync/fake-firebase.js` antes do `mtsync.js`,
desligar o registro do SW e servir com `python3 servir.py 8713`; no console:
`await __fake.auth.signInWithEmailAndPassword('x@exemplo.com')`. `window.__cm` expõe ST, BANCO, QIDX, irAba.

## Erratas da administração (10/10/2026, fl-v6) — `mterrata.js`
Mesma integração do ClínicaMed (ver o CLAUDE.md de lá). A administração corrige ou tira do ar uma questão
sinalizada (admin.html → Sinalizações) e responde a quem sinalizou. `mterrata.js` (fonte única em
`~/Documents/Claude/_mterrata/`, não editar a cópia) busca as erratas na função `mtSinal` (op `erratas`, app
`flashmed`), guarda em `localStorage["mterr:flashmed"]` e o app aplica ANTES de desenhar (`aplicaErratas`).
- `BANCO_BASE` = `window.BANCO` intacto (e `QBASE`, índice dele por chave); `BANCO`/`QIDX` = vista das VISÍVEIS.
  A chave `_ch` sai do enunciado ORIGINAL, antes da errata: corrigir o enunciado não solta o progresso.
- Gabarito corrigido: `okH(q,h)` reavalia respostas antigas só na EXIBIÇÃO (h.alt = índice no banco); o histórico
  salvo não muda. `acerta(q,j)`: gabarito -1 (anulada) aceita qualquer resposta. `cadaResposta`/`nVistas`/`nErros`
  contam sem as ocultas; `recontaBanco()` refaz NREAIS/BANCAS/NQ_AREA quando chega errata nova da rede.
- `ordemQuestoes` preserva as chaves ocultas na ordem salva. Simulado EM CURSO com questão tirada do ar: ela sai
  da prova, a chave fica em `s.tiradas` e a resposta dada continua em `s.res`.
- Prova na íntegra: `nEx(e)` desconta de `EXAMES[].n` as questões daquela edição tiradas do ar (o número no
  seletor "Prova" e no cartão da prova). Questão importada (`orig`: clinicamed/cirurgiamed/radiotitulo) segue a
  chave DESTE app: errata feita no ClínicaMed não chega aqui; corrigir na origem e rodar `importa.py`, ou fazer a
  errata também para o flashmed no painel.
- Errata é remendo: a correção definitiva vai para o banco e depois se desfaz a errata no painel. Mudar o
  enunciado no banco muda a chave.
