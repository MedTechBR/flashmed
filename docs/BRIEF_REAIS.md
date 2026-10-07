# Brief — questões de prova real para o ClínicaMed

Você recebe um lote de questões extraídas VERBATIM de cadernos oficiais públicos (Revalida/INEP,
ENARE pré-requisito em Clínica Médica/EBSERH-FGV, USP/FUVEST especialidades clínicas e ano
adicional). O gabarito (`gab`, índice 0-based) é o OFICIAL DEFINITIVO. Seu trabalho: triar e escrever
os campos editoriais. O app é de estudo de CLÍNICA MÉDICA para título de especialista, R+ e residentes.

## 1. Triagem — para cada questão decida INCLUIR ou DESCARTAR

DESCARTE (e registre o motivo) quando:
- não é clínica médica de adulto: pediatria/neonatologia, ginecologia e obstetrícia, cirurgia geral e
  especialidades cirúrgicas (inclui trauma/ATLS, abdome agudo cirúrgico, hérnia, ortopedia), oftalmo, ORL;
- depende de figura/imagem/tabela/traçado que NÃO está no texto (ex.: "a imagem a seguir", "o ECG
  abaixo" sem descrição suficiente para responder);
- o gabarito oficial contraria a diretriz VIGENTE hoje (setembro de 2026) — ensinar o erro é pior que
  não ter a questão. Diga qual diretriz e o que mudou;
- o texto saiu truncado ou embaralhado na extração (frase cortada, alternativa misturada);
- tem mais de uma resposta defensável.

INCLUA clínica médica e o que o edital de título cobre: cardio, pneumo, nefro/eletrólitos, gastro/hepato,
endócrino, hemato, infecto, reumato, neuro, onco, geriatria/paliativos, psiquiatria, dermatologia na
clínica, emergência clínica/UTI, e SUS/ética/medicina preventiva e epidemiologia aplicadas ao adulto.

## 2. Campos de cada questão incluída

- `q` e `alts`: COPIE EXATAMENTE como vieram. Não reescreva, não corrija estilo, não reordene. Única
  exceção: artefato evidente de extração (ex.: "kg/m2" pode virar "kg/m²", "mm3" → "mm³"; palavra partida
  por hifenização "pronto- socorro" → "pronto-socorro"). Nada além disso.
- `gab`: mantenha o valor recebido (índice 0-based do gabarito oficial). NUNCA altere.
- `tema`: um de cardio, emergencias, infecto, pneumo, gastro, endocrino, nefro, neuro, sus, hemato,
  reumato, geriatria, onco, derma, psiq.
- `cenario`: amb (ambulatório), enf (enfermaria), emg (emergência/urgência), uti.
- `comp`: dx (diagnóstico), tto (tratamento/conduta), urg (urgência/emergência), prev (prevenção/seguimento).
- `nivel`: r1 (essencial), r2 (intermediário), r3 (avançado), tit (nível prova de título).
  Revalida costuma ser r1/r2; ENARE pré-requisito e USP especialidades clínicas, r2/r3/tit.
- `base`: diretriz/documento que sustenta a resposta, com NOME e ANO (4 dígitos obrigatórios), a versão
  VIGENTE. Ex.: "ESC Guidelines for the management of atrial fibrillation, 2024". Não invente sigla nem
  ano: em dúvida, confira na web (WebSearch/WebFetch). Diretrizes já verificadas neste projeto: GINA 2026,
  GOLD 2026, Surviving Sepsis 2026, ADA 2026, KDIGO 2024, AHA/ASA AVC 2026, ESC IC 2026, AHA RCP 2025,
  MS Dengue 2024 (6ª ed.), Diretriz Brasileira de Hipertensão 2025, ESC FA 2024, ACC/AHA SCA 2025,
  AHA/ACC TEP 2026, PCDT HIV 2024, Manual de Tuberculose MS 2019, PCDT IST 2022, Baveno VII 2022,
  EASL, ACR/EULAR vigentes, IMWG 2014, ASH, Beers 2023, MS mamografia 2025 (40 anos, decisão compartilhada).
- `coment`: 150 a 700 caracteres, português, explica POR QUE a oficial está certa e o raciocínio
  clínico, citando o critério/número decisivo e a diretriz. Tom de manual, frases diretas.
- `porAlt`: uma frase por alternativa, na MESMA ordem de `alts`, cada uma com mais de 20 caracteres.
  A da correta começa com "Correta: ". As demais dizem por que estão erradas (não repita a pergunta).
- `fonte`: copie o objeto recebido (`{"banca":..., "ano":...}`).

Regras de escrita (valem para coment e porAlt): **sem travessão (—, –)** — use vírgula, dois-pontos,
parênteses ou ponto; sem emoji; sem "Neste caso, é importante ressaltar"; sem negrito/markdown.

## 3. Saída

Escreva DOIS arquivos (e só eles):
1. `lotes-questoes/leva<NNN>-reais-<sufixo>.json`: lista JSON das questões incluídas, cada uma com as
   chaves q, alts, gab, tema, cenario, comp, nivel, base, coment, porAlt, fonte (nesta ordem).
2. `provas-reais/relatorios/<sufixo>.json`: `{"incluidas": N, "descartadas": [{"id":..., "motivo":...}]}`.

Antes de terminar, rode:
`python3 -c "import json;d=json.load(open('<arquivo da leva>'));assert all(len(x['porAlt'])==len(x['alts']) and len(x['coment'])>=150 and any(c.isdigit() for c in x['base']) for x in d);print(len(d))"`
e corrija o que falhar. Não edite banco.js, leituras nem outros arquivos. Não rode monta_banco.py.
No resumo final, informe: incluídas, descartadas por motivo (contagem), e qualquer gabarito oficial
que você achou discutível mas manteve (com o porquê).
