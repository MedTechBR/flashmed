# Brief — calibrar o tamanho das alternativas nas questões autorais do FlashMed

Problema medido: nas levas autorais `lotes-questoes/leva3NN-*.json` a alternativa correta quase nunca é a mais
longa (0 a 4% em várias levas). Por acaso, com 5 alternativas, seria ~20%. "Nunca marque a mais longa" vira
regra que o aluno explora. Objetivo: em cada leva, a correta passa a ser a mais longa em ~22% das questões.

Entrada: `/private/tmp/claude-501/-Users-matheusparente/d1c1341d-46fc-4d0a-b1fb-752b21d4f876/scratchpad/calibra_lista.json`
(gerada por `python3 docs/calibra_comprimento.py --lista ...`): para cada item, `arquivo`, `indice` (posição na
lista JSON da leva), a correta, o maior distrator, os tamanhos e `alvo_correta` = [mínimo, máximo] de caracteres
para a NOVA correta (2 a 8% maior que o maior distrator).

O que fazer em cada item, editando a leva no lugar (só aquele item):
1. Reescreva a ALTERNATIVA CORRETA (`alts[gab]`) acrescentando um detalhe verdadeiro, preciso e útil (um
   número, o critério, a via, o prazo), até cair dentro de `alvo_correta`. Ela tem de continuar correta e
   inequívoca; não acrescente "sempre", "apenas", "pode", "geralmente". Mantenha o estilo das outras.
2. Se não der para alongar sem forçar, encurte o MAIOR distrator (mantendo o erro dele por conteúdo) até a
   correta ficar 2 a 8% maior que todos.
3. Não mude `gab`, a ordem das alternativas, o enunciado, `coment` nem os outros distratores além do previsto.
   Se o detalhe novo da correta merecer, ajuste a frase "Correta: ..." do `porAlt` correspondente.
4. Sem travessão, sem markdown.

Depois de terminar, rode `cd /Users/matheusparente/Documents/Claude/flashmed && python3 docs/calibra_comprimento.py`
e confira que cada leva ficou entre 18 e 26% (com "ajustar 0"); e rode `python3 monta_banco.py | tail -3` (tem de
dizer "OK: nenhum erro duro"). Não edite nenhum outro arquivo. Resumo final curto: quantas alteradas por leva.
