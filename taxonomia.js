/* FlashMed — taxonomia do conteúdo (preparatório ENARE / ENAMED).

   Fonte do formato: ENAMED (INEP), que desde 2025/26 é a prova objetiva do ENARE de acesso direto:
   100 questões objetivas, 5 horas, 20 questões em cada uma de 5 áreas (Clínica Médica, Cirurgia
   Geral, Ginecologia e Obstetrícia, Pediatria e Medicina de Família e Comunidade), com Saúde Mental
   e Saúde Coletiva como temas TRANSVERSAIS distribuídos dentro delas. Aqui Saúde Mental e Saúde
   Coletiva/SUS viram grandes áreas próprias para estudo e filtro; no simulado ENAMED elas entram
   no bloco de MFC e Saúde Coletiva (ver FORMATOS no index.html).

   `grande` = grande área (GRANDES abaixo)
   `area`   = id da subárea, que é o campo `tema` de cada questão (filtro principal do app)
   `peso`   = incidência esperada numa prova de 100 questões no formato ENAMED. ESTIMATIVA:
              recalibrar pela contagem das provas reais classificadas (Painel → "Incidência real").
   `sub`    = subtemas, usados no filtro fino e no índice das leituras.
   Radiologia é aprofundamento: peso 0, fora dos simulados no formato da prova. */

window.GRANDES=[
 {"id":"clinica","nome":"Clínica Médica","curto":"Clínica","cor":"#2563EB","ic":"heartbeat"},
 {"id":"cirurgia","nome":"Cirurgia Geral","curto":"Cirurgia","cor":"#4F46E5","ic":"cut"},
 {"id":"go","nome":"Ginecologia e Obstetrícia","curto":"GO","cor":"#DB2777","ic":"gender-female"},
 {"id":"ped","nome":"Pediatria","curto":"Pediatria","cor":"#EA580C","ic":"baby-carriage"},
 {"id":"mfc","nome":"Medicina de Família e Comunidade","curto":"MFC","cor":"#16A34A","ic":"home-heart"},
 {"id":"coletiva","nome":"Saúde Coletiva e SUS","curto":"SUS","cor":"#0891B2","ic":"building-hospital"},
 {"id":"mental","nome":"Saúde Mental","curto":"Mental","cor":"#9333EA","ic":"brain"},
 {"id":"imagem","nome":"Radiologia (aprofundamento)","curto":"Radiologia","cor":"#475569","ic":"radioactive"}
];

window.TAXONOMIA=[
{"id":"cardio","grande":"clinica","nome":"Cardiologia","peso":3,"sub":["Hipertensão arterial","Síndrome coronária aguda","Insuficiência cardíaca","Fibrilação atrial e arritmias","Valvopatias","Dislipidemia e risco cardiovascular","Endocardite, miocardite e pericardite"]},
{"id":"emergencias","grande":"clinica","nome":"Emergências e terapia intensiva","peso":2,"sub":["Parada cardiorrespiratória","Choque e sepse","Insuficiência respiratória","Intoxicações","Paciente instável"]},
{"id":"infecto","grande":"clinica","nome":"Infectologia","peso":2.5,"sub":["HIV e infecções oportunistas","Tuberculose","Arboviroses","Doenças tropicais e endemias","Infecções bacterianas","Antimicrobianos","Imunizações do adulto"]},
{"id":"pneumo","grande":"clinica","nome":"Pneumologia","peso":1.5,"sub":["Asma","DPOC","Pneumonia","Tromboembolismo pulmonar","Derrame pleural","Nódulo e câncer de pulmão"]},
{"id":"gastro","grande":"clinica","nome":"Gastroenterologia e hepatologia","peso":1.5,"sub":["Hepatites virais","Cirrose e complicações","Doença do refluxo e dispepsia","Doença inflamatória intestinal","Diarreias","Hemorragia digestiva"]},
{"id":"endocrino","grande":"clinica","nome":"Endocrinologia","peso":2,"sub":["Diabetes","Emergências do diabetes","Tireoide","Adrenal e hipófise","Obesidade","Osteoporose e cálcio"]},
{"id":"nefro","grande":"clinica","nome":"Nefrologia e eletrólitos","peso":1.5,"sub":["Injúria renal aguda","Doença renal crônica","Glomerulopatias","Distúrbios hidroeletrolíticos","Distúrbios ácido-básicos"]},
{"id":"neuro","grande":"clinica","nome":"Neurologia","peso":1.5,"sub":["AVC","Cefaleias","Epilepsia","Demências","Neuropatias e doenças neuromusculares","Coma e rebaixamento"]},
{"id":"hemato","grande":"clinica","nome":"Hematologia","peso":1,"sub":["Anemias","Leucemias e linfomas","Hemostasia e trombose","Transfusão"]},
{"id":"reumato","grande":"clinica","nome":"Reumatologia","peso":1,"sub":["Artrite reumatoide","Lúpus","Gota","Vasculites","Espondiloartrites"]},
{"id":"onco","grande":"clinica","nome":"Oncologia clínica","peso":0.5,"sub":["Emergências oncológicas","Rastreamento de câncer","Síndromes paraneoplásicas"]},
{"id":"geriatria","grande":"clinica","nome":"Geriatria e cuidados paliativos","peso":1,"sub":["Avaliação geriátrica","Delirium","Polifarmácia e Beers","Quedas","Cuidados paliativos"]},
{"id":"derma","grande":"clinica","nome":"Dermatologia","peso":0.5,"sub":["Hanseníase","Farmacodermias","Lesões elementares","Câncer de pele"]},

{"id":"trauma","grande":"cirurgia","nome":"Trauma e queimaduras","peso":5,"sub":["Atendimento inicial (ATLS)","Via aérea e choque no trauma","Trauma de tórax","Trauma abdominal e pélvico","TCE e trauma raquimedular","Queimaduras"]},
{"id":"periop","grande":"cirurgia","nome":"Perioperatório, complicações e infecção","peso":2.5,"sub":["Avaliação pré-operatória","Resposta metabólica ao trauma","Hidratação e nutrição","Complicações pós-operatórias","Infecção de sítio cirúrgico e antibioticoprofilaxia","Anestesia e analgesia"]},
{"id":"abdome","grande":"cirurgia","nome":"Abdome agudo","peso":3,"sub":["Apendicite","Colecistite e colangite","Pancreatite aguda","Obstrução intestinal","Diverticulite","Isquemia mesentérica","Perfuração"]},
{"id":"hernias","grande":"cirurgia","nome":"Hérnias e parede abdominal","peso":1.5,"sub":["Hérnia inguinal","Hérnia femoral","Hérnias ventrais e incisionais","Hérnia encarcerada e estrangulada"]},
{"id":"digestivo","grande":"cirurgia","nome":"Cirurgia do aparelho digestivo","peso":2.5,"sub":["Esôfago","Estômago e cirurgia bariátrica","Intestino delgado","Cólon e reto","Doenças orificiais","Hemorragia digestiva"]},
{"id":"hepatobiliar","grande":"cirurgia","nome":"Fígado, vias biliares e pâncreas","peso":2,"sub":["Colelitíase e coledocolitíase","Icterícia obstrutiva","Tumores hepáticos","Pâncreas"]},
{"id":"cabeca","grande":"cirurgia","nome":"Cabeça, pescoço e cirurgia endócrina","peso":1,"sub":["Nódulo de tireoide","Paratireoide","Adrenal cirúrgica","Massas cervicais"]},
{"id":"cironco","grande":"cirurgia","nome":"Oncologia cirúrgica e pele","peso":1,"sub":["Câncer gástrico","Câncer colorretal","Melanoma e tumores de pele","Sarcomas"]},
{"id":"especialidades","grande":"cirurgia","nome":"Vascular, urologia, tórax, ortopedia e pediátrica","peso":1.5,"sub":["Doença arterial periférica e aneurisma","Trombose venosa","Urologia","Cirurgia torácica","Ortopedia e fraturas","Cirurgia pediátrica"]},

{"id":"obstetricia","grande":"go","nome":"Pré-natal, parto e puerpério","peso":5,"sub":["Diagnóstico de gravidez e pré-natal","Modificações gravídicas","Assistência ao parto","Partograma e distocias","Puerpério e lactação","Vitalidade fetal"]},
{"id":"obstpat","grande":"go","nome":"Intercorrências obstétricas","peso":5,"sub":["Síndromes hipertensivas","Diabetes na gestação","Hemorragias da primeira metade","Hemorragias da segunda metade e pós-parto","Prematuridade e ruptura de membranas","Infecções na gestação","Isoimunização e gemelaridade","Restrição de crescimento"]},
{"id":"ginecologia","grande":"go","nome":"Ginecologia geral e endócrina","peso":3.5,"sub":["Sangramento uterino anormal","Amenorreias","Síndrome dos ovários policísticos","Endometriose e dor pélvica","Miomatose","Climatério"]},
{"id":"ginonco","grande":"go","nome":"Oncologia ginecológica e mama","peso":3,"sub":["Rastreamento do câncer do colo","Lesões precursoras e HPV","Câncer de mama e rastreamento","Doenças benignas da mama","Câncer de endométrio","Massas anexiais e câncer de ovário"]},
{"id":"gininfec","grande":"go","nome":"Infecções genitais e IST","peso":2,"sub":["Vulvovaginites","Úlceras genitais e sífilis","Uretrites e cervicites","Doença inflamatória pélvica","HPV e verrugas"]},
{"id":"reprodutiva","grande":"go","nome":"Planejamento reprodutivo e violência sexual","peso":1.5,"sub":["Métodos contraceptivos","Critérios de elegibilidade (OMS)","Contracepção de emergência","Infertilidade","Violência sexual e aborto legal"]},

{"id":"neonato","grande":"ped","nome":"Neonatologia","peso":4.5,"sub":["Reanimação neonatal","Icterícia neonatal","Desconforto respiratório","Sepse neonatal","Triagens neonatais","Infecções congênitas (TORCHS)","Recém-nascido pré-termo"]},
{"id":"puericultura","grande":"ped","nome":"Puericultura e imunização","peso":4.5,"sub":["Crescimento","Desenvolvimento","Aleitamento materno","Alimentação complementar","Calendário vacinal","Suplementação de ferro e vitaminas"]},
{"id":"pedinfecto","grande":"ped","nome":"Infecções na infância","peso":4.5,"sub":["Doenças exantemáticas","Infecções de vias aéreas superiores","Pneumonia","Bronquiolite","Meningite","Diarreia e desidratação","Infecção urinária","Parasitoses"]},
{"id":"pedemerg","grande":"ped","nome":"Emergências pediátricas","peso":3,"sub":["Suporte avançado de vida pediátrico","Choque e sepse","Crise asmática","Convulsão febril e estado de mal","Intoxicações e acidentes","Maus-tratos"]},
{"id":"pedgeral","grande":"ped","nome":"Pediatria geral e especialidades","peso":3.5,"sub":["Asma e alergias","Cardiopatias congênitas","Nefrologia pediátrica","Endocrinologia pediátrica e puberdade","Hematologia e oncologia pediátrica","Gastroenterologia pediátrica","Adolescência"]},

{"id":"aps","grande":"mfc","nome":"Atenção primária e Estratégia Saúde da Família","peso":2.5,"sub":["Atributos da APS","PNAB e equipes","Território e adscrição","Acesso e acolhimento","Coordenação do cuidado e regulação"]},
{"id":"ferramentas","grande":"mfc","nome":"Abordagem familiar e centrada na pessoa","peso":1.5,"sub":["Método clínico centrado na pessoa","Genograma e ecomapa","Ciclo de vida familiar","Registro clínico (SOAP e CIAP-2)","Comunicação e notícia difícil"]},
{"id":"rastreamento","grande":"mfc","nome":"Prevenção, rastreamento e prevenção quaternária","peso":2,"sub":["Níveis de prevenção","Rastreamento de câncer","Rastreamento cardiovascular e metabólico","Prevenção quaternária","Check-up"]},
{"id":"cronicas","grande":"mfc","nome":"Condições crônicas e queixas comuns na APS","peso":2,"sub":["Hipertensão e diabetes na APS","Multimorbidade e polifarmácia","Lombalgia e dor crônica","Tabagismo","Queixas comuns"]},
{"id":"grupos","grande":"mfc","nome":"Ciclos de vida e populações na APS","peso":1.5,"sub":["Saúde do idoso","Saúde do homem","População LGBTQIA+","População em situação de rua","Saúde indígena e rural","Visita e atenção domiciliar"]},

{"id":"sus","grande":"coletiva","nome":"SUS: legislação, princípios e organização","peso":3,"sub":["Constituição e Lei 8.080","Lei 8.142 e controle social","Princípios e diretrizes","Financiamento","Redes de Atenção à Saúde","Políticas nacionais"]},
{"id":"epidemio","grande":"coletiva","nome":"Epidemiologia e indicadores","peso":2,"sub":["Medidas de frequência","Indicadores de saúde","Transição epidemiológica","Epidemias e surtos","Causalidade"]},
{"id":"bioestat","grande":"coletiva","nome":"Estudos, bioestatística e MBE","peso":2,"sub":["Tipos de estudo","Medidas de associação","Testes diagnósticos","Vieses e confusão","Estatística inferencial","Níveis de evidência"]},
{"id":"vigilancia","grande":"coletiva","nome":"Vigilância em saúde e imunização","peso":1.5,"sub":["Notificação compulsória","Vigilância epidemiológica e sanitária","Investigação de surto","Programa Nacional de Imunizações"]},
{"id":"etica","grande":"coletiva","nome":"Ética médica, bioética e medicina legal","peso":1.5,"sub":["Código de Ética Médica","Sigilo e prontuário","Documentos médicos e atestados","Declaração de óbito","Bioética","Medicina legal"]},
{"id":"trabalho","grande":"coletiva","nome":"Saúde do trabalhador","peso":0.5,"sub":["Doenças relacionadas ao trabalho","CAT e afastamento","Acidente com material biológico"]},

{"id":"humor","grande":"mental","nome":"Depressão, ansiedade e transtornos afins","peso":1.5,"sub":["Depressão","Transtornos de ansiedade","TOC e trauma","Transtornos somatoformes","Luto"]},
{"id":"psicoses","grande":"mental","nome":"Psicoses e transtorno bipolar","peso":1,"sub":["Esquizofrenia","Transtorno bipolar","Antipsicóticos e estabilizadores","Primeiro episódio psicótico"]},
{"id":"drogas","grande":"mental","nome":"Álcool, tabaco e outras drogas","peso":1,"sub":["Uso de álcool","Abstinência alcoólica","Opioides, cocaína e outras","Redução de danos"]},
{"id":"emergpsiq","grande":"mental","nome":"Emergências psiquiátricas e suicídio","peso":1,"sub":["Risco de suicídio","Agitação psicomotora","Delirium","Síndrome neuroléptica maligna e serotoninérgica"]},
{"id":"raps","grande":"mental","nome":"RAPS, legislação e saúde mental na APS","peso":0.5,"sub":["Rede de Atenção Psicossocial","Lei 10.216","Internação involuntária","Matriciamento"]},
{"id":"psiqinf","grande":"mental","nome":"Saúde mental da infância e outros transtornos","peso":0.5,"sub":["TDAH","Transtorno do espectro autista","Transtornos alimentares","Transtornos de personalidade","Insônia"]},

{"id":"radiologia","grande":"imagem","nome":"Radiologia e diagnóstico por imagem","peso":0,"sub":["Tórax","Neurorradiologia","Abdome e digestório","Urogenital","Musculoesquelético","Mama","Ultrassonografia e Doppler","Física, contraste e segurança","Pediatria","Intervenção"]}
];

/* Cenário em que a questão se passa. */
window.CENARIOS=[
 {"id":"amb","nome":"Ambulatório e APS"},
 {"id":"enf","nome":"Enfermaria"},
 {"id":"emg","nome":"Pronto-socorro"},
 {"id":"uti","nome":"UTI"},
 {"id":"cc","nome":"Centro cirúrgico e sala de parto"}
];

/* O que a questão cobra de você. */
window.COMPETENCIAS=[
 {"id":"dx","nome":"Diagnóstico"},
 {"id":"tto","nome":"Tratamento/Conduta"},
 {"id":"urg","nome":"Urgência/Emergência"},
 {"id":"prev","nome":"Prevenção/Seguimento"},
 {"id":"bas","nome":"Bases, gestão e conceitos"}
];

/* Os `id` são os mesmos do ClínicaMed (r1/r2/r3/tit) para que as questões importadas
   não precisem de tradução. Rótulos pensados para quem se prepara para ENARE/ENAMED. */
window.NIVEIS=[
 {"id":"r1","nome":"Essencial","desc":"O que todo médico generalista resolve: reconhecer, estabilizar e conduzir."},
 {"id":"r2","nome":"Intermediário","desc":"Diagnóstico diferencial mais fino, indicação de exames e seguimento."},
 {"id":"r3","nome":"Avançado","desc":"Nuance de diretriz, nível das provas mais concorridas (USP, R+)."},
 {"id":"tit","nome":"Especialista","desc":"Profundidade de prova de título ou de pré-requisito; aprofundamento."}
];
