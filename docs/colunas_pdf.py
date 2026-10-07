#!/usr/bin/env python3
"""Texto do PDF em ordem de leitura por COLUNA (esquerda inteira, depois direita), página a página.
Os cadernos do Revalida e do ENARE são em duas colunas; o pdftotext mistura as duas.
Uso: python3 colunas.py arquivo.pdf > saida.txt"""
import sys, fitz

doc = fitz.open(sys.argv[1])
for pg in doc:
    w = pg.rect.width
    mid = w / 2
    esq, dir_, cheia = [], [], []
    d = pg.get_text("dict")
    for b in d["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"]).rstrip()
            if not txt.strip():
                continue
            x0, y0, x1, y1 = l["bbox"]
            item = (round(y0, 1), x0, txt)
            if x1 - x0 > w * 0.62:
                cheia.append(item)
            elif x0 < mid - 5:
                esq.append(item)
            else:
                dir_.append(item)
    # linhas de largura total (cabeçalho, título) no topo; depois colunas
    for col in (sorted(cheia), sorted(esq), sorted(dir_)):
        for _, _, t in col:
            print(t)
    print("\f")
