#!/usr/bin/env python3
"""Confere links entre leituras (href="outra.html#ancora"): arquivo e âncora têm de existir.
Criado em 24/09/2026 durante a reescrita das 84 monografias em paralelo, quando uma leitura
reescrita tirava uma âncora que outra usava."""
import re, glob, os, sys
ids = {}
for f in glob.glob('leituras/*.html'):
    ids[os.path.basename(f)] = set(re.findall(r'id="([^"]+)"', open(f).read()))
ruins = []
for f in sorted(glob.glob('leituras/*.html')):
    for alvo, anc in re.findall(r'href="([a-z0-9-]+\.html)(?:#([^"]*))?"', open(f).read()):
        if alvo not in ids:
            ruins.append((os.path.basename(f), alvo, anc, 'arquivo inexistente'))
        elif anc and anc not in ids[alvo]:
            ruins.append((os.path.basename(f), alvo, anc, 'âncora inexistente'))
for r in ruins: print('%s -> %s#%s: %s' % r)
print(len(ruins), 'links quebrados')
sys.exit(1 if ruins else 0)
