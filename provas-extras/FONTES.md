# Provas extras de acesso direto: fontes (07/10/2026)

Cadernos e gabaritos oficiais, públicos e sem login, baixados do site da banca. Texto extraído verbatim
com PyMuPDF (leitura por faixas e colunas; tabela do caderno vira linhas com " | " entre células e
quebra de linha entre linhas; tabela cujas linhas são as alternativas vira uma alternativa por linha,
com o cabeçalho da coluna antes do valor). Os PDFs ficaram no rascunho da sessão, fora do projeto.

## usp25ad: USP 2025 Acesso Direto (FUVEST, Edital COREME/FM nº 01/2024)

- Caderno (Prova A1): https://www.fuvest.br/wp-content/uploads/2024-12-01_rm2025_prova-areasbasicasedeacessodireto_grupo-a1.pdf
- Gabarito: https://www.fuvest.br/wp-content/uploads/2024-12-01_rm2025_gabarito-areasbasicasedeacessodireto.pdf
- Página do acervo: https://www.fuvest.br/acervo-residencia-coreme-sp-2025/
- Acesso em 07/10/2026.
- Sobre o gabarito: a FUVEST não usa os rótulos "preliminar" e "definitivo". No acervo, o gabarito das
  Áreas Básicas e Acesso Direto aparece como "Publicado em 01/12/2024". As outras provas do mesmo
  processo ganharam "Gabarito Retificado em 13/12/2024", depois dos recursos. Este não foi retificado,
  então o de 01/12/2024 é o gabarito que valeu. Não há questão anulada (nenhum "*" no gabarito).
  Conferi as 120 respostas da Prova A1 contra a tabela de correspondência A1/A2/A3 da página 2 do
  gabarito: 120 de 120 batem.
- O caderno tem 120 questões de 4 alternativas. As provas A1, A2 e A3 são as mesmas questões em
  ordem diferente. Usei a A1.
- **Extraídas: 110.** Anuladas: nenhuma.
- **Fora do arquivo (10), porque as alternativas são só imagem e não têm texto:** 16, 17, 63, 76, 84,
  86, 104, 114, 117, 119.
- **Com aviso "figura" (32):** 3, 6, 7, 10, 18, 20, 39, 49, 58, 62, 64, 70, 74, 77, 78, 79, 85, 87, 92,
  93, 95, 96, 99, 100, 101, 105, 106, 109, 110, 112, 118, 120. A 118 está aqui porque o próprio
  caderno diz "IMAGEM REMOVIDA NOS TERMOS DO ESTATUTO DA CRIANÇA E DO ADOLESCENTE".
- Ajustes no texto: nas questões 85 ("Útero") e 95 ("5h 9h 16h"), tirei o rótulo que fica dentro da
  figura e que a extração tinha jogado no meio do enunciado. As tabelas das questões 22, 23, 27, 31,
  32, 43, 44, 65, 106 e 115 foram montadas a partir da tabela do caderno. Na 23, na 65, na 106 e na
  115, as alternativas são as linhas dessa tabela.
- Como conferi: (1) cada frase do enunciado e das alternativas das 110 questões foi procurada no
  texto do PDF. O que não apareceu igual foram só pontos de montagem: células de tabela, a junção do
  texto comum a duas questões com o enunciado e as figuras. (2) Comparei a página das questões 65 a
  69 renderizada com o JSON, olhando enunciado, alternativas e gabarito. (3) Olhei a página da
  questão 86 para confirmar que as alternativas são imagens.

## Tentadas e não usadas

- **UNICAMP 2025 e 2026 Acesso Direto** (Comvest, comvest.unicamp.br/residenciamedica2025/provas.html e
  .../residenciamedica2026/provas.html): a 1ª fase do acesso direto é "Prova Objetiva - respostas
  curtas" (dAD1/dAD2, com "respostas esperadas"), sem alternativas. Não serve para o formato de
  múltipla escolha. As provas de teste da Comvest (tCL, tCir, tPed) são de especialidades com
  pré-requisito, não de acesso direto.
- **USP 2024 Acesso Direto** (FUVEST, https://www.fuvest.br/wp-content/uploads/rm_2024_a1.pdf, a2, a3;
  gabarito retificado em https://www.fuvest.br/wp-content/uploads/rm2024_gabarito_areas_basicas_acesso-direto_2023-12-18.pdf):
  os três cadernos usam fontes Type3 sem mapeamento de caracteres, então não há texto extraível (o
  mesmo problema do Revalida 2022.1). Para extrair, seria preciso OCR, e o OCR não garante texto
  verbatim.
- **UNIFESP, SUS-SP e PSU-MG/AREMG**: não deu para procurar, porque a cota de 10 buscas acabou nas
  tentativas acima.

## Rodada 2 (07/10/2026): ENAMED 2025 e provas de especialidade do ENARE

Todos com gabarito DEFINITIVO, baixados direto do site da banca (sem login). As questões anuladas
ficaram fora dos JSON. Extração: `docs/colunas_pdf.py` + `docs/extrai_prova.py` (cópia do ClínicaMed
com os cabeçalhos do caderno do ENARE 2025/2026 no LIXO); rodapé "Tipo 1 – código – Página N" tirado
depois por regex.

### enamed25: ENAMED 2025 (INEP), caderno 1
- Caderno: https://download.inep.gov.br/enamed/provas_e_gabaritos/2025_caderno_1_preliminar.pdf
- Gabarito definitivo: https://download.inep.gov.br/enamed/provas_e_gabaritos/2025_gabarito_caderno_1.pdf
  (10 anuladas: 2, 7, 9, 10, 11, 40, 43, 76, 88, 100).
- O caderno usa Calibri Light como fonte CID (Identity-H) SEM tabela ToUnicode: o texto sai em
  glifos. Decodificado glifo a glifo pela tabela de caracteres da Calibri Light instalada com o
  Office (`calibril.ttf`: cmap invertido + ligaduras do GSUB), só nos trechos com códigos de glifo
  (abaixo de 0x20 ou entre 0x100 e 0x4FF). Script: `docs/ferramentas/decod_enamed.py`.
  Conferência: as 49 questões 1 a 50 que também estão no Revalida 2025.2 (texto limpo) saíram
  IDÊNTICAS, enunciado e alternativas; nas 42 que já estavam no banco, o gabarito bate em 42/42.
- No banco, a questão comum às duas provas fica com `fonte.ex = enamed25` e o Revalida 2025.2 em
  `fonte.tb` (monta_banco/importa: provas-extras são registradas primeiro).

### ENARE pré-requisito / ano adicional (EBSERH/FGV), Tipo 1
Uma prova por especialidade de base, aplicada a todas as áreas de atuação daquela base (a de
Neonatologia é a mesma da Medicina do Adolescente, por exemplo).
- 2024/2025: https://mapa-vagas-enare-ebserh.conhecimento.fgv.br/provas-gabaritos/medica/ +
  `area-de-atuacao/AREA DE ATUACAO - NEONATOLOGIA (ATNeonatT01).pdf` (Pediatria),
  `ano-adicional/ANO ADICIONAL - GINECOLOGIA E OBSTETRICIA R4 (AAGINOBST01).pdf`,
  `ano-adicional/ANO ADICIONAL - MEDICINA DE FAMILIA E COMUNIDADE R3 (AAMEFACOT01).pdf`,
  `area-de-atuacao/AREA DE ATUACAO - PSIQUIATRIA DA INFANCIA E ADOLESCENCIA (ATPsInAdT01).pdf`;
  gabarito definitivo "ENARE 2024 Gabarito Definitivo - Medica.pdf" (blocos "... - TIPO 1").
- 2025/2026: https://storage.googleapis.com/website-enare-2025/assets/provas/res-med/ +
  `area-at/p2e058-...neonatologia...`, `ano-ad/p1e010-...ginecologia-e-obstetricia-r4...`,
  `ano-ad/p1e014-...medicina-de-familia-e-comunidade-r3...`, `area-at/p2e067-...psiquiatria-da-infancia...`
  (lista em assets/provas/nomes-dos-arquivos.csv); gabaritos definitivos em
  assets/provas/gabaritos/enare2025-medicos-gabarito-definitivo-{area-de-atuacao,ano-adicional}.pdf.
- Questões de Clínica Médica dessas provas foram descartadas na triagem (pedido de 07/10: aumentar
  as outras áreas). Relatórios: docs/relatorios/real_19 a real_35.

### Tentadas e não usadas (rodada 2)
- Revalida 2020: só há gabarito PRELIMINAR público em PDF; o definitivo ficou na página do participante.
