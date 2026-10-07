#!/usr/bin/env python3
"""Viés de tamanho AO CONTRÁRIO: nas autorais do FlashMed (leva3NN) a correta quase nunca é a alternativa
mais longa (0 a 4% em algumas levas). Isso também é explorável: "nunca marque a mais longa" vira regra.
Por acaso, com 5 alternativas, a correta é a mais longa em ~20%. Alvo: 18 a 26% por leva.

Uso:
  python3 docs/calibra_comprimento.py            → relatório por leva
  python3 docs/calibra_comprimento.py --lista F  → grava em F as questões a ajustar (as de menor folga:
                                                   a edição mínima que faz a correta passar a mais longa)
O ajuste é feito por um redator (texto clínico), nunca por script: alongar a CORRETA com um detalhe preciso
e verdadeiro, ou encurtar o distrator mais longo sem mudar o erro dele, até a correta ficar 2 a 8% maior
que o maior distrator.
"""
import json, glob, sys, random, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVO = 0.22

def stats(d):
    longa = [i for i, x in enumerate(d) if len(x["alts"][x["gab"]]) > max(len(a) for j, a in enumerate(x["alts"]) if j != x["gab"])]
    return longa

def main():
    out = []
    for arq in sorted(glob.glob(os.path.join(RAIZ, "lotes-questoes", "leva3*.json"))):
        d = json.load(open(arq, encoding="utf-8"))
        longa = stats(d)
        falta = max(0, round(ALVO * len(d)) - len(longa))
        cands = []
        for i, x in enumerate(d):
            if i in longa: continue
            Lc = len(x["alts"][x["gab"]]); M = max(len(a) for j, a in enumerate(x["alts"]) if j != x["gab"])
            cands.append((M / Lc, i, Lc, M))
        cands.sort()
        escolhidas = cands[:falta]
        print(f"{os.path.basename(arq)}: {len(d)} questões, correta mais longa em {len(longa)} ({round(len(longa)/len(d)*100)}%), ajustar {falta}")
        for r, i, Lc, M in escolhidas:
            x = d[i]
            out.append({"arquivo": os.path.basename(arq), "indice": i, "enunciado_inicio": x["q"][:90],
                        "correta": x["alts"][x["gab"]], "maior_distrator": max((a for j, a in enumerate(x["alts"]) if j != x["gab"]), key=len),
                        "tam_correta": Lc, "tam_maior_distrator": M,
                        "alvo_correta": [int(M * 1.02) + 1, int(M * 1.08)]})
    if "--lista" in sys.argv:
        dest = sys.argv[sys.argv.index("--lista") + 1]
        json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{len(out)} questões para ajustar → {dest}")

if __name__ == "__main__":
    main()
