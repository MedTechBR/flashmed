# Adendo ao BRIEF_AUTORAIS_FM.md: rodada 2 (07/10/2026)

Leia primeiro `docs/BRIEF_AUTORAIS_FM.md` inteiro: tudo lá vale, com as mudanças abaixo.

## Não repetir o que o banco já tem
O banco tem ~3.900 questões. Antes de escrever, veja o que já existe nos seus temas:
```
cd /Users/matheusparente/Documents/Claude/flashmed && python3 -c "
import json,re,sys,collections
b=json.loads(re.sub(r'^window.BANCO=|;\s*$','',open('banco.js').read()))
T=set(sys.argv[1:])
for q in b:
  if q['tema'] in T: print(q['tema'],'|',q.get('sub',''),'|',q['q'][:110])
" TEMA1 TEMA2 ...
```
Escreva sobre pontos que faltam ou que aparecem pouco, e nunca o mesmo caso com outra roupa. Cubra
o tema de forma ampla (diagnóstico, conduta, complicação, prevenção), no nível do que o ENAMED e o
ENARE cobram de quem termina a graduação.

## Viés de tamanho (corrige o brief anterior)
A rodada 1 errou para o outro lado: a correta quase nunca era a mais longa, e isso também vira dica.
Alvo do seu arquivo: a correta é a alternativa mais longa em **18 a 26%** das questões (por acaso seria
~20%). Mantenha os distratores entre ~85% e ~115% do tamanho da correta. O verificador do brief tem
`assert longa/len(d)<=0.35`; acrescente você mesmo a conferência de que ficou entre 0,18 e 0,26.

## Fontes
- As leituras do próprio app já foram escritas com as normas conferidas em 2026: use-as como mapa e
  conferência (`leituras/*.html`, `leituras/cir/*.html`, `leituras/cm/*.html`). Não copie frases delas.
- Trauma: ATLS 11ª edição está em `~/Documents/Livros/ATLS - Suporte Avançado de Vida no Trauma 11a edição.pdf`
  (extraia o capítulo com `pdftotext -f N -l M`). Pontos já conferidos: hemotórax e toracotomia decididos
  pela fisiologia, reposição de queimado a 2 mL/kg/%SCQ no adulto (Parkland modificada), sangue
  precoce e equilibrado em vez de cristaloide em volume.
- No máximo **3 buscas** (WebSearch/WebFetch) para o trabalho inteiro. Sem fonte confirmada, não faça
  a questão sobre o ponto duvidoso.

## Ritmo
Escreva em partes (10 questões por vez, acrescentando ao arquivo). No fim rode o verificador do brief
e mais:
```
python3 -c "
import json,sys
d=json.load(open(sys.argv[1]));L=0
for x in d:
  a=x['alts'];g=x['gab']
  if len(a[g])>max(len(t) for j,t in enumerate(a) if j!=g): L+=1
print('correta mais longa', round(L/len(d)*100),'%'); assert 0.18<=L/len(d)<=0.26
" ARQUIVO
```
