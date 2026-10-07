#!/usr/bin/env python3
"""Escolhe, entre variantes de redação, a que cai na janela de 95–108% do comprimento da correta.

Existe porque corrigir um tell de linguagem quase sempre muda o tamanho da alternativa e reabre o
viés de comprimento. Uso: editar VAR abaixo e rodar. Cada entrada é
(arquivo-sem-extensão, índice da questão, prefixo atual) -> [variantes em ordem de preferência].
"""
import json, glob, sys

def aplica(VAR):
    fora = []
    for arq in sorted(glob.glob("lotes-questoes/leva*.json")):
        nome = arq.split("/")[-1].replace(".json", "")
        b = json.load(open(arq, encoding="utf-8")); mudou = False
        for (f, qi, pref), variantes in VAR.items():
            if f != nome: continue
            q = b[qi]; Lc = len(q["alts"][q["gab"]])
            lo, hi = Lc * 0.95, Lc * 1.08
            for i, a in enumerate(q["alts"]):
                if not a.startswith(pref): continue
                ok = [v for v in variantes if lo <= len(v) <= hi]
                if ok:
                    q["alts"][i] = ok[0]; mudou = True
                else:
                    fora.append((nome, qi + 1, i, round(lo), round(hi),
                                 [(len(v), v[:50]) for v in variantes]))
        if mudou: json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in fora:
        print("SEM VARIANTE NA JANELA:", f[0], f"Q{f[1]} alt{f[2]} alvo {f[3]}-{f[4]}")
        for n, t in f[5]: print(f"    {n}: {t}")
    return len(fora)

if __name__ == "__main__":
    sys.exit(0)
