# Brief — leituras do FlashMed (preparatório ENARE / ENAMED)

O FlashMed (`~/Documents/Claude/flashmed/`) é o app de estudo do MedTech para ENARE e ENAMED. Ele já traz as
99 monografias de Clínica Médica do ClínicaMed (`leituras/cm/`) e as de Cirurgia (`leituras/cir/`). Faltam
as leituras de **Ginecologia e Obstetrícia, Pediatria, Medicina de Família e Comunidade, Saúde Coletiva/SUS
e Saúde Mental**. Você escreve algumas delas. Público: interno e médico recém-formado que vai prestar a
prova de acesso direto à residência. Dono: Matheus, médico, coordenador de internato, lê diretriz e
UpToDate todo dia e reprova texto com cara de blog ou de IA.

## O texto
- **3.000 a 4.500 palavras** por leitura (conte com `sed 's/<[^>]*>/ /g' leituras/ARQ.html | wc -w`).
  É um resumo aprofundado de prova: o que cai, com os números, critérios e condutas exatos, e o porquê.
- **Fonte vigente em outubro de 2026, com ano**, preferindo o documento oficial brasileiro que a banca
  usa: Ministério da Saúde (manuais, Cadernos de Atenção Básica, PCDT, Guia de Vigilância em Saúde,
  calendário do PNI), leis e portarias (planalto.gov.br, bvsms.saude.gov.br), CFM, FEBRASGO, SBP, ABP,
  SBMFC; e internacionais quando a prova brasileira as cobra (OMS, DSM-5-TR, USPSTF, NICE, ISSHP, ILCOR).
  **Número de memória não entra**: dose, corte, prazo, idade e intervalo têm de vir de fonte conferida.
  Onde a norma mudou recentemente, diga o que mudou e quando (é o que a banca adora cobrar).
- **Prosa de médico para médico**, português do Brasil. Explique o raciocínio quando ele decide a
  conduta. Cada seção precisa dizer o que muda a conduta ou o que a prova cobra.
- **Proibido:** travessão (— ou –) na prosa, título e legenda (só em célula vazia de tabela e rótulo de
  mermaid); emoji; "é importante ressaltar", "vale destacar", "neste contexto", "neste texto"; frase de
  efeito ou aforismo de fechamento ("o tempo é cérebro", "não é X, é Y"); título no molde "Assunto:
  manchete" (título e h2 são substantivos: "Pré-eclâmpsia", não "Pré-eclâmpsia: o inimigo silencioso");
  dek que narra o texto ("Este texto percorre..."); h2 numerado; negrito em toda frase; sigla ou
  diretriz inventada; copiar texto de diretriz, livro ou cursinho em bloco.
- **Figuras:** nenhuma imagem de terceiros (direito autoral, app público e pago). Esquema próprio em SVG
  inline é bem-vindo (partograma, curva de crescimento esquemática, genograma de exemplo, fluxo da RAPS,
  linha do tempo da vacinação): fonte `-apple-system,system-ui,sans-serif`, cores `var(--ink)`,
  `var(--ink2)`, `var(--brand)`, `var(--linha)`, `var(--ok)`, `var(--err)`, `var(--avi)`; texto de SVG
  não quebra linha, quebre à mão e confira que nada vaza do viewBox.

## Estrutura do HTML (o validador `python3 valida_leituras.py` confere)
```html
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Título (Fonte ANO)</title>
<link rel="stylesheet" href="_leitura.css?v=1"><script src="_leitura.js?v=1"></script>
<div class="wrap">
<p class="kicker">Grande área · NN min · Fonte principal ANO</p>
<h1>Título</h1>
<p class="dek">O que o texto cobre e por qual fonte, em uma ou duas frases.</p>
<nav class="toc"><b>Sumário</b><ol><li><a href="#id">Seção</a></li>…</ol></nav>
<h2 id="id">Seção</h2>
…
<h2 id="armadilhas">Erros frequentes</h2>   (penúltima)
<h2 id="autoteste">Perguntas de revisão</h2> (última; 5 a 8 <details><summary>pergunta</summary>resposta</details>)
<a class="vaiQuestoes" href="../index.html?area=TEMA#questoes">Treinar questões de …</a>
<footer><b>Fontes primárias</b><ol><li>Referência completa com ano (e link oficial quando houver).</li></ol></footer>
</div>
```
Todo `<h2>` tem `id` e aparece no sumário, na mesma ordem e com o mesmo texto. `TEMA` é um id de
`taxonomia.js` (obstetricia, obstpat, ginecologia, ginonco, gininfec, reprodutiva, neonato, puericultura,
pedinfecto, pedemerg, pedgeral, aps, ferramentas, rastreamento, cronicas, grupos, sus, epidemio, bioestat,
vigilancia, etica, trabalho, humor, psicoses, drogas, emergpsiq, raps, psiqinf).

Componentes (de `leituras/_leitura.css`; veja um modelo pronto em `leituras/cm/parada-cardiaca.html` e
`leituras/cm/dor-toracica.html`):
`table.criterio` (critérios, escores, calendários), `div.rolagem > table` (tabela larga), `div.cx chave`,
`div.cx armadilha`, `div.cx nota`, `div.cx fonte` (primeira linha em `<b>` vira título), `div.ancora`
(questão-âncora: `<b>Questão-âncora</b>` mini-caso `<details><summary>Resposta</summary>…</details>`;
2 a 4 por leitura), `div.sind` (3 blocos `<div><b>O que perguntar</b><ul>…`), `div.compara` (2 a 4
blocos lado a lado), `div.dose` (`<b>…</b><ul>…</ul>`), `ol.passos`, `table.rec` só se a fonte der classe
e nível (transcritos, nunca inventados).

Fluxogramas (mínimo 2 por leitura), mermaid:
```html
<div class="fluxo"><div class="leg"><b>Fluxograma 1</b>Legenda curta</div>
<pre class="mermaid">
flowchart TD
  A["Rótulo entre aspas"] --> B{"Pergunta?"}
  B -->|"sim"| C["Ação"]
</pre></div>
```
Todo rótulo entre aspas, quebra com `<br/>`, nada de parêntese ou vírgula fora das aspas, no máximo 3
nós lado a lado e rótulos curtos (o desenho tem de caber em ~720 px).

## Como trabalhar (vários redatores rodam ao mesmo tempo)
- Escreva o HTML **por seções**: crie o arquivo com o cabeçalho e a primeira seção, depois acrescente uma
  seção por vez (Edit, inserindo antes de `<a class="vaiQuestoes"`), no máximo ~900 palavras por
  acréscimo. Nunca um Write gigante.
- Escreva SÓ os seus arquivos: `leituras/<slug>.html` e `leituras/_entradas_<seu-lote>.json`. Rascunhos
  em `/private/tmp/claude-501/-Users-matheusparente/d1c1341d-46fc-4d0a-b1fb-752b21d4f876/scratchpad/leit-<seu-lote>/`.
- **Não toque** em `leituras.js`, `index.html`, `banco.js`, `taxonomia.js`, `_leitura.css/js`, em
  `leituras/cm/`, `leituras/cir/` nem em leitura de outro redator. Não rode bump, commit ou push.
- **Cota de buscas: no máximo 7 WebSearch/WebFetch para o lote inteiro.** Prefira WebFetch direto no
  documento oficial. Se não conseguir confirmar um número, deixe-o de fora e anote no relatório.

## Fechamento
1. Conte as palavras de cada leitura. 2. `cd ~/Documents/Claude/flashmed && python3 valida_leituras.py`
   tem de sair sem erro nas suas. 3. Escreva `leituras/_entradas_<seu-lote>.json`:
```json
[{"grupo":"Ginecologia e Obstetrícia","f":"pre-natal.html","tipo":"MS 2022 · resumo de prova","area":"obstetricia","min":45,
  "t":"Pré-natal de baixo risco","s":"Duas a quatro linhas com o que o texto cobre e a fonte."}]
```
`grupo` é um de: "Ginecologia e Obstetrícia", "Pediatria", "Medicina de Família e Comunidade",
"Saúde Coletiva e SUS", "Saúde Mental". `min` = palavras ÷ 80. `s` = o mesmo texto do dek.
4. Relatório final curto: arquivos, palavras, fluxogramas, fontes usadas (com ano) e o que ficou "a
   conferir".
