#!/usr/bin/env python3
"""Sobe a versão do app em UM lugar só.

O bug que isto conserta: o sw.js usa stale-while-revalidate nos estáticos, então
bumpar só o CACHE faz o usuário receber o banco novo apenas na SEGUNDA visita —
e quem não tem o SW registrado (primeira visita, aba anônima) pega o banco.js da
cache HTTP do navegador, que não expira. Sem ?v= na tag, o deploy fica invisível.

Uso: python3 bump.py   (roda antes do commit; bumpa sw.js e index.html juntos)
"""
import re, pathlib, sys

sw = pathlib.Path('sw.js'); idx = pathlib.Path('index.html')
m = re.search(r'const CACHE="fl-v(\d+)"', sw.read_text())
if not m:
    sys.exit('não achei const CACHE="fl-vN" em sw.js')
novo = int(m.group(1)) + 1

s = re.sub(r'const CACHE="fl-v\d+"', f'const CACHE="fl-v{novo}"', sw.read_text())
# a lista PRE precisa carregar o MESMO ?v= que a página pede: o handler casa por URL
# completa, então "./banco.js" precacheado nunca atende "./banco.js?v=25" e o app
# ficaria sem offline até a primeira visita online cachear a URL versionada.
s = re.sub(r'"\./([A-Za-z0-9_\-/]+\.(?:js|css))(?:\?v=\d+)?"',
           lambda m: f'"./{m.group(1)}?v={novo}"', s)
sw.write_text(s)

t = idx.read_text()
# acrescenta ou atualiza ?v=N nos scripts locais (ignora http/https)
# o (?!https?:|/) deixa de fora os scripts da raiz do site (/_mtfb.js, /_mtauth.js): eles
# são de outro repo e versionar aqui só geraria cache miss a cada deploy
t, n = re.subn(r'<script src="(?!https?:|/)([^"?]+)(?:\?v=\d+)?"',
               lambda x: f'<script src="{x.group(1)}?v={novo}"', t)
idx.write_text(t)

# as páginas de leitura pedem _leitura.css/_leitura.js; sem ?v= elas divergem do PRE
nl = 0
for f in sorted(pathlib.Path('leituras').rglob('*.html')):
    s = f.read_text()
    s2 = re.sub(r'(href|src)="((?:\.\./)?_leitura\.(?:css|js))(?:\?v=\d+)?"',
                lambda m: f'{m.group(1)}="{m.group(2)}?v={novo}"', s)
    if s2 != s:
        f.write_text(s2); nl += 1
print(f'fl-v{novo} — sw.js, {n} scripts em index.html, {nl} leituras')
