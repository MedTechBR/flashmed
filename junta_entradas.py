#!/usr/bin/env python3
"""Funde os `leituras/_entradas_*.json` dos agentes no leituras.js e apaga os sidecars.

Existe porque cinco agentes escrevendo no mesmo leituras.js colidem: cada um deposita a própria
entrada num arquivo só dele e este script costura. Entrada já existente (mesmo `f`) é ATUALIZADA
no lugar, preservando a posição dentro do grupo; entrada nova entra no fim do grupo da área.
"""
import json, pathlib, re, sys

LJ = pathlib.Path('leituras.js')
src = LJ.read_text()
novas = []
for f in sorted(pathlib.Path('leituras').glob('_entradas_*.json')):
    try:
        d = json.loads(f.read_text())
    except Exception as e:
        sys.exit(f'{f}: JSON inválido — {e}')
    novas += d if isinstance(d, list) else [d]
if not novas:
    sys.exit('nenhum _entradas_*.json para juntar')

def bloco(e):
    esc = lambda s: str(s).replace('\\', '\\\\').replace('"', '\\"')
    return (f' {{f:"{e["f"]}", tipo:"{esc(e["tipo"])}", area:"{e["area"]}", min:{int(e["min"])},\n'
            f'  t:"{esc(e["t"])}",\n'
            f'  s:"{esc(e["s"])}"}},\n')

trocadas, acrescentadas = 0, []
for e in novas:
    alvo = re.search(r'^ \{f:"' + re.escape(e['f']) + r'".*?\},\n', src, re.S | re.M)
    if alvo:
        src = src[:alvo.start()] + bloco(e) + src[alvo.end():]
        trocadas += 1
    else:
        acrescentadas.append(e)

for e in acrescentadas:
    # entra depois da última leitura da mesma área
    ult = None
    for m in re.finditer(r'^ \{f:"[^"]+".*?area:"' + re.escape(e['area']) + r'".*?\},\n', src, re.S | re.M):
        ult = m
    if ult:
        src = src[:ult.end()] + bloco(e) + src[ult.end():]
    else:
        src = src.rstrip().rstrip(']').rstrip() + '\n' + bloco(e) + '];\n'

LJ.write_text(src)
for f in pathlib.Path('leituras').glob('_entradas_*.json'):
    f.unlink()
print(f'{trocadas} entradas atualizadas, {len(acrescentadas)} acrescentadas; sidecars apagados')
