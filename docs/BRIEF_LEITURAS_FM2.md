# Adendo ao BRIEF_LEITURAS_FM.md: rodada 2 (07/10/2026)

Leia primeiro `docs/BRIEF_LEITURAS_FM.md` inteiro: tudo lá vale, com as mudanças abaixo.

- **Cirurgia agora tem leituras próprias do FlashMed.** `grupo` = "Cirurgia"; `area` = um id de Cirurgia
  em `taxonomia.js` (trauma, periop, abdome, hernias, digestivo, hepatobiliar, cabeca, cironco,
  especialidades). O kicker diz "Cirurgia · NN min · Fonte ANO".
- **Não repita leitura que já existe.** Antes de escrever, abra a lista (`ls leituras/ leituras/cm/
  leituras/cir/`) e leia por cima as vizinhas do seu tema. Se um pedaço do seu tema já está bem coberto
  em outra leitura, trate dele em um parágrafo e aponte para ela com link relativo
  (`<a href="cir/atendimento-inicial-trauma.html">…</a>` ou `cm/…`), e use o espaço no que falta.
- Fontes locais (sem gastar busca): ATLS 11ª ed. em `~/Documents/Livros/ATLS - Suporte Avançado de Vida
  no Trauma 11a edição.pdf` (use `pdftotext -f N -l M` só no capítulo); `~/Documents/Livros/Medicina_de_Emergencia_Abordagem_Pratica_USP_HC_FM_250401_183332.pdf`
  (Medicina de Emergência, USP, para urgências cirúrgicas e urológicas, conferindo o ano da edição).
  Livros servem para conferir número e conduta; o texto é seu, nunca transcrito.
- **Cota: no máximo 5 buscas** (WebSearch/WebFetch) para o lote inteiro. Download direto de PDF oficial
  com `curl` a partir de um link que você já tem também conta como uma busca.
- Rascunhos em `/private/tmp/claude-501/-Users-matheusparente/d1c1341d-46fc-4d0a-b1fb-752b21d4f876/scratchpad/leit-<seu-lote>/`.
