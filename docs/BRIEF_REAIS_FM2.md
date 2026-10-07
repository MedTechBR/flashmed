# Adendo ao BRIEF_REAIS_FM.md: rodada 2 (07/10/2026)

Leia primeiro `docs/BRIEF_REAIS_FM.md` inteiro: tudo lá vale. Este adendo só acrescenta.

## As provas desta rodada
- **ENAMED 2025** (INEP, caderno 1, gabarito DEFINITIVO; questões anuladas já foram tiradas). É a prova
  de acesso direto que o app prepara: 4 alternativas, nível r1/r2. As questões 1 a 50 do caderno que já
  estão no banco (iguais às do Revalida 2025.2) não vieram para você.
  O texto deste caderno foi DECODIFICADO de uma fonte sem tabela de caracteres (glifo a glifo, conferido
  contra as 49 questões iguais do Revalida, todas idênticas). Se notar letra trocada ou palavra estranha
  que seja claramente erro de decodificação, corrija só aquela letra e registre em `gabaritos_discutiveis`
  com a nota "correção de decodificação: X → Y".
- **ENARE pré-requisito/ano adicional (EBSERH/FGV), edições 2024/2025 e 2025/2026**: as provas de
  Pediatria (aplicada às áreas de atuação pediátricas), Ginecologia e Obstetrícia, Medicina de Família e
  Comunidade e Psiquiatria. 5 alternativas, gabarito DEFINITIVO, prova para quem JÁ fez a residência da
  área. Nível: r2 ou r3 na maioria, `tit` quando for detalhe de especialista que o ENAMED não cobraria.
  O app já sabe que estas provas são de especialidade (ficam fora do simulado ENAMED por padrão), então
  inclua mesmo as difíceis, desde que corretas e atuais.

## Clínica Médica fica de fora (exceto no ENAMED)
O banco já tem muita Clínica Médica. Nas provas do ENARE (sobretudo a de MFC, que cobra clínica geral),
**descarte** a questão cujo `tema` correto seria uma subárea de Clínica (cardio, emergencias, infecto,
pneumo, gastro, endocrino, nefro, neuro, hemato, reumato, onco, geriatria, derma), com o motivo
"clínica médica: fora do escopo desta rodada". Antes de descartar, veja se ela não é de MFC de verdade:
HAS, DM, dislipidemia, tabagismo, queixa comum, multimorbidade conduzidas na APS = `cronicas`; rastreamento
= `rastreamento`; idoso/acamado na APS = `grupos`. Dissecção de aorta, arritmia, insuficiência renal em
hemodiálise etc. são Clínica.
Na prova de Psiquiatria, demência e delirium entram como Saúde Mental quando o foco é psiquiátrico
(diagnóstico diferencial com depressão, manejo comportamental, antipsicótico): use `humor` ou `psicoses`
conforme o caso; neurologia pura (tratamento de Parkinson, AVC) é Clínica e sai.
No **ENAMED 2025** as questões de Clínica ENTRAM normalmente (é a prova-alvo e o app monta ela na íntegra).

## Pesquisa e ritmo
No máximo **3 buscas** (WebSearch/WebFetch) para o lote. Escreva a leva em partes (10 questões por vez,
acrescentando ao arquivo), nunca uma saída gigante de uma vez.
