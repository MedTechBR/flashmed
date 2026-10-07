/* Provas-alvo do FlashMed. Regras conferidas em 07/10/2026:
   ENAMED → INEP (Portaria e edital 2025; estrutura repetida em 2026). Desde o ENARE 2025/2026, a prova
            objetiva do ENARE de ACESSO DIRETO é o próprio ENAMED. ENAMED 2025: 19/10/2025. ENAMED 2026 e
            ENARE 2026/2027: 13/09/2026 (resultado do acesso direto em 04/12/2026).
   Revalida → INEP, 1ª etapa objetiva com 100 questões; em 2025 parte das questões foi comum ao ENAMED.
   `data` nula: o app não inventa data de prova futura; a pessoa informa a dela em Ajustes. */
window.PROVAS=[
{"id":"enamed","nome":"ENAMED / ENARE acesso direto","org":"INEP · EBSERH",
 "data":null,"oque":"Prova objetiva","q":100,"alts":4,
 "regra":"100 questões objetivas de 4 alternativas em 5 horas, 20 em cada área: Clínica Médica, Cirurgia Geral, Ginecologia e Obstetrícia, Pediatria e Medicina de Família e Comunidade. Saúde Mental e Saúde Coletiva entram como temas transversais dentro delas. A nota é calculada por Teoria de Resposta ao Item e o resultado vale para o ENARE de acesso direto (quem atingiu nível proficiente em edição anterior pode reaproveitar a nota).",
 "edital":"INEP, ENAMED 2025 e 2026; Edital ENARE 2026/2027"},
{"id":"revalida","nome":"Revalida, 1ª etapa","org":"INEP",
 "data":null,"oque":"Prova objetiva","q":100,"alts":4,
 "regra":"100 questões objetivas nas mesmas cinco grandes áreas. Quem passa faz a 2ª etapa de habilidades clínicas. Em 2025 o Revalida 2025.2 teve questões em comum com o ENAMED.",
 "edital":"INEP, Revalida (download.inep.gov.br/revalida/provas_e_gabaritos)"},
{"id":"institucionais","nome":"Provas próprias (USP, SUS-SP, UNICAMP e outras)","org":"bancas institucionais",
 "data":null,"oque":"Prova objetiva","q":null,"alts":5,
 "regra":"Formato varia por instituição, em geral 100 a 120 questões de 4 ou 5 alternativas nas cinco grandes áreas. O banco traz a USP (FUVEST) em acesso direto e especialidades.",
 "edital":""}
];
