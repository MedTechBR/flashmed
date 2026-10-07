# Brief — questões AUTORAIS e cartões para o FlashMed (preparatório ENARE / ENAMED)

O FlashMed é o app de estudo do MedTech para o ENARE e o ENAMED (desde 2025/26 a prova objetiva do ENARE
de acesso direto É o ENAMED: 100 questões, 5 horas, 20 em cada área: Clínica Médica, Cirurgia, GO,
Pediatria e Medicina de Família e Comunidade, com Saúde Mental e Saúde Coletiva transversais). O banco já
tem ~2.700 questões (muitas de prova real), mas Saúde Mental, MFC, Saúde Coletiva, GO e Pediatria precisam
de questões novas. Você escreve questões NOVAS, do zero, no nível ENARE/ENAMED.

## Proibido
- Copiar ou parafrasear questão de cursinho, de livro ou de prova (nem "trocar um termo"). Escreva do zero.
- Escrever conduta de memória quando ela pode ter mudado. A régua é a norma VIGENTE em outubro de 2026,
  com fonte e ano. Para o Brasil, prefira o documento oficial: Ministério da Saúde (cadernos de atenção
  básica, manuais, PCDT, Guia de Vigilância em Saúde, calendário do PNI), leis e portarias, CFM,
  FEBRASGO, SBP, ABP, SBMFC; internacionais quando a prova brasileira as usa (OMS, USPSTF, NICE, DSM-5-TR).
  Exemplos de mudança recente a CONFERIR (não presumir): rastreamento do colo por DNA-HPV (MS/INCA
  2024/2025), mamografia a partir dos 40 (MS 2025, Lei 15.284/2025), HPV em dose única (2024), PNAB e
  financiamento da APS (2024/2025: eMulti no lugar do NASF, novo cofinanciamento), lista de notificação
  compulsória vigente, Código de Ética Médica (Res. CFM 2.217/2018 e alterações).
- Copiar texto de diretriz em bloco.

## Formato de cada questão (chaves nesta ordem)
```json
{"q": "...", "alts": ["...","...","...","...","..."], "gab": 0, "tema": "humor", "sub": "...",
 "cenario": "amb", "comp": "tto", "nivel": "r1", "base": "Documento, ANO", "coment": "...",
 "porAlt": ["Correta: ...", "...", "...", "...", "..."]}
```
- `q`: caso clínico curto e realista (40 a 120 palavras) OU pergunta direta quando o assunto é
  conceito/legislação. Termine com a pergunta. Nada de "assinale a INCORRETA" em excesso (no máximo 1 em 10).
- `alts`: 5 alternativas plausíveis, mesma classe gramatical, sem "todas as anteriores". Distratores
  erram por CONTEÚDO (conduta de outro cenário, prazo/dose/corte trocado, conceito vizinho), nunca
  por vagueza. Sem prefixo de letra.
- Viés de tamanho (o defeito nº 1 de questão escrita por IA): a correta NÃO pode ser a mais longa nem
  a mais detalhada. Escreva distratores tão completos quanto a correta (entre ~85% e ~115% do tamanho
  dela). Em cerca de metade das questões, a correta deve ser MAIS CURTA que pelo menos dois distratores.
  Sem "sempre/nunca/apenas" concentrados nos distratores; sem hedge ("pode", "geralmente") só na correta;
  todos os distratores com acentuação normal.
- `gab`: índice 0-4 da correta. Distribua: no seu arquivo, cada posição (0 a 4) deve ser a correta em
  ~20% das questões.
- `tema`, `cenario` (amb, enf, emg, uti, cc), `comp` (dx, tto, urg, prev, bas), `nivel` (r1 essencial,
  r2 intermediário, r3 avançado; quase tudo r1/r2 para ENARE/ENAMED).
- `sub`: subtema curto (2 a 6 palavras).
- `base`: documento com NOME e ANO de 4 dígitos. Ex.: "Ministério da Saúde. Política Nacional de Atenção
  Básica (Portaria 2.436/2017, consolidada), 2017", "Lei 10.216/2001", "DSM-5-TR, 2022".
- `coment`: 250 a 800 caracteres: por que a correta está certa, o critério/número decisivo, a fonte.
- `porAlt`: uma frase por alternativa (mais de 20 caracteres), mesma ordem; a correta começa com "Correta: ".

## Cartões (repetição espaçada)
Além das questões, escreva 25 cartões dos seus temas: `{"tema":"humor","a":"pergunta curta","b":"resposta
com o número/critério e a fonte com ano"}`. Frente até 120 caracteres, verso até 320.

## Escrita
Português do Brasil, tom de manual de estudo. Sem travessão (— ou –) em nenhum campo; sem emoji;
sem markdown; sem frases de efeito; sem metanarrativa ("esta questão avalia"); não cite letra de
alternativa no comentário (a ordem exibida muda).

## Pesquisa na web
No MÁXIMO 4 buscas (WebSearch/WebFetch) para o trabalho inteiro: use para conferir as normas que podem ter
mudado e que você vai cobrar. Prefira WebFetch direto no gov.br/saude, bvsms.saude.gov.br, planalto.gov.br,
portal.cfm.org.br. Se não conseguir confirmar uma norma, não faça questão sobre o ponto duvidoso.

## Saída (escreva SÓ estes arquivos)
1. `/Users/matheusparente/Documents/Claude/flashmed/lotes-questoes/leva3NN-<slug>.json` (lista JSON).
2. `/Users/matheusparente/Documents/Claude/flashmed/docs/flash_<slug>.json` (lista JSON dos cartões).
Escreva em partes se precisar (por exemplo, 10 questões por vez, acrescentando ao arquivo), nunca uma
saída gigante de uma vez.

Antes de terminar, rode e corrija até passar:
```
python3 -c "
import json,re,sys,statistics,collections
d=json.load(open(sys.argv[1])); longa=0; folgas=[]
for i,x in enumerate(d):
  a=x['alts']; g=x['gab']; Lc=len(a[g])
  assert len(a)==5 and len(set(a))==5, i
  assert len(x['porAlt'])==5 and x['porAlt'][g].startswith('Correta: '), i
  assert 250<=len(x['coment'])<=900 and re.search(r'(19|20)\d\d',x['base']), i
  assert x['cenario'] in 'amb enf emg uti cc'.split() and x['comp'] in 'dx tto urg prev bas'.split() and x['nivel'] in 'r1 r2 r3 tit'.split(), i
  assert not re.search('[—–]', json.dumps(x,ensure_ascii=False)), i
  for j,t in enumerate(a):
    assert 0.6<=len(t)/Lc<=1.7, (i,j,'comprimento')
  m=max(len(t) for j,t in enumerate(a) if j!=g)
  if Lc>m: longa+=1; folgas.append((Lc-m)/m*100)
print(len(d),'questões; correta mais longa em',round(longa/len(d)*100),'% (alvo <= 35%); gabarito',sorted(collections.Counter(x['gab'] for x in d).items()))
assert longa/len(d)<=0.35
" /Users/matheusparente/Documents/Claude/flashmed/lotes-questoes/leva3NN-<slug>.json
```
Não edite nenhum outro arquivo. Resumo final curto: nº de questões por tema, nº de cartões, normas
conferidas na web (com ano) e pontos que você evitou por não conseguir confirmar.
