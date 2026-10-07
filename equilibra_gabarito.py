#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redistribui a posição do gabarito para que A–E fiquem equilibrados NO BANCO INTEIRO.

⚠️ RODAR ANTES DE PUBLICAR A LEVA. Depois de o app estar em uso, NÃO rodar de novo: as
respostas gravadas guardam o ÍNDICE da alternativa escolhida, e remexer na ordem faria o
histórico apontar para a alternativa errada.

⚠️ O equilíbrio é GLOBAL, não por arquivo. A versão anterior (herdada do TráfegoTítulo)
distribuía com `[i % 5 for i in range(n)]` dentro de cada leva: com levas de 3 ou 4
questões isso nunca chegava às posições D e E, e o banco inteiro saiu sem nenhuma
resposta na letra E — viés que o aluno aprende a explorar em prova de 5 alternativas.
Por isso este script recebe TODAS as levas de uma vez:

    python3 equilibra_gabarito.py lotes-questoes/leva*.json
"""
import json, sys, random

def equilibra(arquivos, semente=20260904):
    rnd = random.Random(semente)
    carga = [(arq, json.load(open(arq, encoding="utf-8"))) for arq in arquivos]
    total = sum(len(b) for _, b in carga)
    alvos = [i % 5 for i in range(total)]          # uniforme sobre o BANCO todo
    rnd.shuffle(alvos)
    it = iter(alvos)
    for arq, b in carga:
        for q in b:
            alts, pa, g = q["alts"], q.get("porAlt"), q["gab"]
            alvo = next(it)
            if len(alts) != 5:                      # formato inesperado: não mexe
                continue
            if alvo == g:
                continue
            outras_a = [a for i, a in enumerate(alts) if i != g]
            q["alts"] = outras_a[:alvo] + [alts[g]] + outras_a[alvo:]
            if pa:
                outras_p = [p for i, p in enumerate(pa) if i != g]
                q["porAlt"] = outras_p[:alvo] + [pa[g]] + outras_p[alvo:]
            q["gab"] = alvo
        json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dist = {}
    for _, b in carga:
        for q in b:
            dist[q["gab"]] = dist.get(q["gab"], 0) + 1
    print(f"{total} questões em {len(carga)} levas — " +
          ", ".join(f"{chr(65+k)}:{dist.get(k,0)}" for k in range(5)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("uso: python3 equilibra_gabarito.py lotes-questoes/leva*.json  (passe TODAS as levas)")
    equilibra(sys.argv[1:])
