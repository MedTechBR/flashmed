# Brief — questões de prova real para o FlashMed (preparatório ENARE / ENAMED)

O FlashMed é o app de estudo do MedTech para ENARE e ENAMED: 5 grandes áreas da prova (Clínica Médica,
Cirurgia Geral, Ginecologia e Obstetrícia, Pediatria, Medicina de Família e Comunidade) mais Saúde Mental e
Saúde Coletiva/SUS como áreas próprias. Público: estudante do internato e médico recém-formado.

Você recebe um lote de questões extraídas VERBATIM de cadernos oficiais públicos (Revalida/INEP, ENARE/
EBSERH-FGV, USP/FUVEST). O gabarito (`gab`, índice 0-based) é o OFICIAL DEFINITIVO. Seu trabalho: triar e
escrever os campos editoriais. `pista_area` é uma classificação antiga e grosseira; use só como pista.

## 1. Triagem — INCLUIR ou DESCARTAR (registre o motivo de cada descarte)

DESCARTE quando:
- depende de figura, imagem, gráfico, tabela ou traçado que NÃO está no texto ("a imagem a seguir", "o
  gráfico abaixo", "conforme a figura") e o texto sozinho não basta para responder;
- o gabarito oficial contraria a diretriz/norma VIGENTE hoje (outubro de 2026). Ensinar o erro é pior que
  não ter a questão. Diga qual documento vigente e o que mudou. Atenção a mudanças recentes de verdade
  (exemplos a CONFERIR, não a presumir): rastreamento do colo do útero no Brasil por teste de DNA-HPV
  (Diretrizes Brasileiras, MS/INCA 2024/2025); mamografia a partir dos 40 anos (MS 2025 + Lei 15.284/2025);
  calendário vacinal do PNI (HPV em dose única desde 2024, mudanças de 2025/2026); reanimação neonatal
  (SBP 2022, atualizações posteriores); AHA 2025 de RCP; CHA2DS2-VA (ESC 2024);
- o texto saiu truncado ou embaralhado na extração (frase cortada, alternativa misturada com outra);
- tem mais de uma resposta defensável, ou nenhuma.
Questões antigas cujo conteúdo segue válido ENTRAM: o ano da prova não é motivo de descarte.

## 2. Campos de cada questão incluída (nesta ordem)

- `q` e `alts`: COPIE EXATAMENTE. Não reescreva, não corrija estilo, não reordene. Única exceção: artefato
  evidente de extração ("kg/m2" → "kg/m²", "mm3" → "mm³", "pronto- socorro" → "pronto-socorro", espaço
  duplo). Nada além disso.
- `gab`: o valor recebido. NUNCA altere.
- `tema`: UM id desta lista (subárea):
  Clínica: cardio, emergencias, infecto, pneumo, gastro, endocrino, nefro, neuro, hemato, reumato, onco,
  geriatria, derma.
  Cirurgia: trauma (inclui queimaduras), periop (pré e pós-operatório, complicações, infecção, anestesia),
  abdome (abdome agudo), hernias, digestivo (esôfago, estômago, delgado, cólon, reto, ânus, hemorragia
  digestiva cirúrgica), hepatobiliar (vias biliares, fígado, pâncreas eletivos), cabeca (tireoide,
  paratireoide, pescoço, adrenal cirúrgica), cironco (oncologia cirúrgica, pele), especialidades (vascular,
  urologia, tórax, ortopedia, cirurgia pediátrica).
  GO: obstetricia (pré-natal, parto, puerpério, vitalidade fetal, lactação), obstpat (intercorrências:
  hipertensão, diabetes, hemorragias, prematuridade, RPMO, infecções na gestação, gemelaridade,
  isoimunização, CIUR), ginecologia (SUA, amenorreia, SOP, endometriose, mioma, climatério), ginonco
  (colo, mama, endométrio, ovário, rastreamento), gininfec (vulvovaginites, IST, DIP), reprodutiva
  (contracepção, infertilidade, violência sexual, aborto legal).
  Pediatria: neonato, puericultura (crescimento, desenvolvimento, aleitamento, alimentação, vacinas),
  pedinfecto, pedemerg, pedgeral (doenças crônicas e especialidades, adolescência).
  MFC: aps (atributos, PNAB, ESF, território, acesso), ferramentas (MCCP, genograma, ecomapa, ciclo de vida,
  SOAP/CIAP-2, comunicação), rastreamento (níveis de prevenção, rastreamentos, prevenção quaternária),
  cronicas (HAS/DM e queixas comuns conduzidas na APS, multimorbidade, tabagismo), grupos (idoso, homem,
  LGBTQIA+, população de rua, indígena, rural, atenção domiciliar).
  Saúde Coletiva: sus (legislação, princípios, financiamento, RAS, políticas), epidemio (medidas,
  indicadores, surtos, causalidade), bioestat (desenhos de estudo, medidas de associação, testes
  diagnósticos, vieses, MBE), vigilancia (notificação, vigilância, PNI como política), etica (CEM,
  bioética, documentos, declaração de óbito, medicina legal), trabalho (saúde do trabalhador).
  Saúde Mental: humor (depressão, ansiedade, TOC, TEPT, luto), psicoses (esquizofrenia, bipolar,
  antipsicóticos), drogas (álcool, tabaco e outras), emergpsiq (suicídio, agitação, SNM), raps (RAPS, Lei
  10.216, matriciamento), psiqinf (TDAH, TEA, alimentares, personalidade, insônia).
  Critério: a área de quem resolveria o caso na vida real. Vacina de criança = puericultura; vacina como
  política/cobertura = vigilancia. Hipertensão na gestação = obstpat. Depressão atendida na UBS = humor.
  Criança com abdome agudo cirúrgico = especialidades. Questão de APS sobre hipertensão = cronicas.
- `sub`: subtema curto em português (2 a 6 palavras), por exemplo "Pré-eclâmpsia com sinais de gravidade".
- `cenario`: amb (ambulatório e APS), enf (enfermaria), emg (pronto-socorro), uti, cc (centro cirúrgico
  e sala de parto).
- `comp`: dx (diagnóstico), tto (tratamento/conduta), urg (urgência/emergência), prev (prevenção/
  seguimento), bas (bases, gestão, legislação, epidemiologia, conceitos).
- `nivel`: r1 (essencial), r2 (intermediário), r3 (avançado), tit (especialista). Revalida e ENARE acesso
  direto: quase sempre r1/r2. USP acesso direto: r2/r3. Provas de especialidade/pré-requisito: r3/tit.
- `base`: documento que sustenta a resposta, com NOME e ANO de 4 dígitos, na versão VIGENTE. Ex.:
  "Ministério da Saúde. Caderno de Atenção Básica nº 32 (pré-natal de baixo risco), 2012, com Manual de
  Gestação de Alto Risco, 2022". Não invente sigla nem ano. Para SUS e ética, a lei/resolução com número
  e ano ("Lei 8.080/1990", "Resolução CFM 2.217/2018, Código de Ética Médica"). Já conferidas em outros
  apps do MedTech (pode usar): GINA 2026, GOLD 2026, Surviving Sepsis 2026, ADA 2026, KDIGO 2024,
  AHA/ASA AVC 2026, ESC IC 2026, AHA RCP 2025, MS Dengue 2024 (6ª ed.), Diretriz Brasileira de Hipertensão
  2025, ESC FA 2024, PCDT HIV 2024, Manual de Tuberculose MS 2019, PCDT IST 2022, Beers 2023, ATLS 11ª ed.
  (2025), Tokyo Guidelines 2018. Para o resto, confira na web antes de citar.
- `coment`: 200 a 800 caracteres, português, explica POR QUE a oficial está certa e o raciocínio, citando
  o critério ou número decisivo e o documento. Tom de manual de estudo, frases diretas.
- `porAlt`: uma frase por alternativa, na MESMA ordem de `alts`, cada uma com mais de 20 caracteres. A da
  correta começa com "Correta: ". As demais dizem por que estão erradas.
- `fonte`: copie o objeto recebido sem mudar nada.
- `pid`: copie o recebido.

Regras de escrita (coment e porAlt): sem travessão (— ou –), use vírgula, dois-pontos, parênteses ou
ponto; sem emoji; sem markdown nem negrito; sem frases de efeito ("o tempo é cérebro", "não é X, é Y");
sem "Neste caso, é importante ressaltar"; sem metanarrativa ("esta questão avalia..."). Não cite letra
da alternativa ("a letra C"): as alternativas são exibidas em outra ordem em alguns modos.

## 3. Pesquisa na web

Você tem no MÁXIMO 3 buscas (WebSearch/WebFetch) para o lote inteiro. Use só para o que for decisivo e
duvidoso (norma que pode ter mudado). Para o resto, use o que você sabe com segurança e as diretrizes já
conferidas acima. Na dúvida sobre o gabarito oficial contra a diretriz vigente, descarte e explique.

## 4. Saída — escreva SÓ estes dois arquivos

1. `/Users/matheusparente/Documents/Claude/flashmed/lotes-questoes/leva2NN-reais-NN.json` (NN = número do
   lote): lista JSON das questões incluídas com as chaves pid, q, alts, gab, tema, sub, cenario, comp,
   nivel, base, coment, porAlt, fonte.
2. `/Users/matheusparente/Documents/Claude/flashmed/docs/relatorios/real_NN.json`:
   `{"incluidas": N, "descartadas": [{"pid":..., "motivo":...}], "gabaritos_discutiveis": [{"pid":..., "nota":...}]}`.

Antes de terminar, rode e corrija o que falhar:
```
python3 -c "
import json,re,sys
d=json.load(open(sys.argv[1]))
T='cardio emergencias infecto pneumo gastro endocrino nefro neuro hemato reumato onco geriatria derma trauma periop abdome hernias digestivo hepatobiliar cabeca cironco especialidades obstetricia obstpat ginecologia ginonco gininfec reprodutiva neonato puericultura pedinfecto pedemerg pedgeral aps ferramentas rastreamento cronicas grupos sus epidemio bioestat vigilancia etica trabalho humor psicoses drogas emergpsiq raps psiqinf'.split()
for x in d:
  assert x['tema'] in T, x['pid']; assert x['cenario'] in 'amb enf emg uti cc'.split(), x['pid']
  assert x['comp'] in 'dx tto urg prev bas'.split(), x['pid']; assert x['nivel'] in 'r1 r2 r3 tit'.split(), x['pid']
  assert len(x['porAlt'])==len(x['alts']) and 200<=len(x['coment'])<=900 and re.search(r'(19|20)\d\d',x['base']), x['pid']
  assert x['porAlt'][x['gab']].startswith('Correta: '), x['pid']
  assert not re.search('[—–]', x['coment']+' '.join(x['porAlt'])), x['pid']
print(len(d),'ok')" <arquivo da leva>
```
Não edite nenhum outro arquivo. No resumo final (curto): incluídas, descartadas por motivo (contagem) e
os gabaritos oficiais discutíveis que você manteve, com o porquê.
