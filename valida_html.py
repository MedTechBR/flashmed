#!/usr/bin/env python3
"""Checa a sintaxe dos <script> INLINE do index.html.

Existe por um erro que custou uma sessão inteira de depuração: uma substituição de texto
comeu o `async` de `async function pintaAjustes()`, deixando um `await` órfão dentro dela.
O bloco inteiro parou de executar, o app subiu sem nenhuma aba — e nada disso aparece em
`node --check` (que não lê HTML) nem no validador de leituras.

Uso: python3 valida_html.py   (roda antes do bump; sai != 0 se houver erro)
"""
import re, pathlib, subprocess, tempfile, os, sys

html = pathlib.Path('index.html').read_text()
blocos = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)
falhas = 0
for i, b in enumerate(blocos):
    f = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False); f.write(b); f.close()
    r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
    if r.returncode:
        falhas += 1
        print(f'bloco inline #{i}:')
        for l in r.stderr.splitlines()[:5]: print('   ' + l)
    os.unlink(f.name)

for js in sorted(pathlib.Path('.').glob('*.js')):
    r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
    if r.returncode:
        falhas += 1
        print(f'{js}:')
        for l in r.stderr.splitlines()[:5]: print('   ' + l)

print(f'{len(blocos)} blocos inline + arquivos .js — {falhas} com erro de sintaxe')
sys.exit(1 if falhas else 0)
