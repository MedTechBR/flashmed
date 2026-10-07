#!/usr/bin/env python3
"""Mapeia o número global da questão (Qn do validador) para arquivo e índice na leva.
Uso: python3 acha.py 177 178   → imprime arquivo, índice e as alternativas com os tells marcados."""
import json, glob, re, sys
A = re.compile(r"\b(sempre|nunca|jamais|apenas|somente|exclusivamente|tod[oa]s?|nenhum[a]?|qualquer|quaisquer|invariavelmente)\b", re.I)
C = re.compile(r"\b(pode(m)?|geralmente|costuma(m)?|tende(m)?|recomenda-se|habitualmente|em geral)\b", re.I)
AC = re.compile(r"[àáâãéêíóôõúç]", re.I)

def main(alvos):
    n = 0
    for arq in sorted(glob.glob("lotes-questoes/leva*.json")):
        for qi, q in enumerate(json.load(open(arq, encoding="utf-8"))):
            n += 1
            if n not in alvos: continue
            g = q["gab"]
            print(f"\n=== Q{n} → {arq} índice {qi} (gab={g}, correta={len(q['alts'][g])} chars)")
            for j, a in enumerate(q["alts"]):
                t = []
                if A.search(a): t.append("ABS")
                if C.search(a): t.append("CAU")
                if len(a) > 60 and not AC.search(a): t.append("SEM-AC")
                print(f" {'*' if j == g else ' '}{j} [{len(a):>3}] {' '.join(t):10} {a}")

if __name__ == "__main__":
    main({int(x) for x in sys.argv[1:]})
