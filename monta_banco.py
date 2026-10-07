#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta banco.js a partir de lotes-questoes/leva*.json (ordem alfabética) e valida.

banco.js é GERADO — não editar à mão. Para mexer numa questão, edite a leva
correspondente e rode: python3 monta_banco.py

Levas:
  leva001–003  importadas (importa.py) do ClínicaMed, CirurgiaMed e RadioTítulo: NÃO editar aqui,
               corrigir no app de origem e rodar importa.py de novo
  leva2NN      provas reais comentadas para o FlashMed (GO, pediatria, preventiva, MFC, mental...)
  leva3NN      autorais do FlashMed

O que este montador faz além de concatenar:
  - normaliza `fonte` das provas reais pela tabela docs/exames.py + docs/ordem.json: cada questão de
    prova ganha {banca, ano, prova, ex, n} no mesmo formato, venha de qual app vier (o ClínicaMed
    antigo gravava "Revalida 2024" sem dizer se era 2024.1 ou 2024.2);
  - tira campos de trabalho (`pid`) e duplicatas exatas (mesma chave);
  - gera exames.js: a lista das provas com quantas questões cada uma tem no banco (aba Simulado,
    "Provas na íntegra").
"""
import glob, json, os, subprocess, sys
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ); sys.path.insert(0, os.path.join(RAIZ, "docs"))
from valida_banco import chave_q, normtxt
from exames import EXAMES, fonte as fonte_de

def main():
    ordem = json.load(open(os.path.join(RAIZ, "docs", "ordem.json"), encoding="utf-8"))
    banco, vistos, dup = [], set(), 0
    for arq in sorted(glob.glob(os.path.join(RAIZ, "lotes-questoes", "leva*.json"))):
        leva = json.load(open(arq, encoding="utf-8"))
        print(f"  {os.path.basename(arq)}: {len(leva)} questões")
        for q in leva:
            k = chave_q(q)
            if k in vistos: dup += 1; continue
            vistos.add(k)
            q = {kk: v for kk, v in q.items() if kk != "pid"}
            f = q.get("fonte")
            if isinstance(f, dict):
                o = ordem.get(k) or ordem.get("p:" + normtxt(q["q"])[:150])
                ex = (o or {}).get("ex") or f.get("ex")
                if ex in EXAMES:
                    n = (o or {}).get("n") or f.get("n")
                    q["fonte"] = fonte_de(ex, n)
            banco.append(q)
    with open(os.path.join(RAIZ, "banco.js"), "w", encoding="utf-8") as f:
        f.write("window.BANCO=")
        json.dump(banco, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"banco.js gerado: {len(banco)} questões ({dup} duplicatas descartadas)\n")

    # provas na íntegra
    por = {}
    for q in banco:
        f = q.get("fonte") or {}
        if f.get("ex"): por.setdefault(f["ex"], []).append(q)
    ex = []
    for k, (b, a, p, tipo) in EXAMES.items():
        qs = por.get(k, [])
        if not qs: continue
        ex.append({"id": k, "nome": p, "banca": b, "ano": a, "tipo": tipo, "n": len(qs),
                   "comNumero": sum(1 for q in qs if q["fonte"].get("n"))})
    ex.sort(key=lambda e: (-e["ano"], e["nome"]))
    with open(os.path.join(RAIZ, "exames.js"), "w", encoding="utf-8") as f:
        f.write("/* GERADO por monta_banco.py: provas reais presentes no banco (aba Simulado → Provas na íntegra). */\n")
        f.write("window.EXAMES=" + json.dumps(ex, ensure_ascii=False, indent=0) + ";\n")
    print("exames.js: " + ", ".join(f"{e['nome']} ({e['n']})" for e in ex) + "\n")

    # migração do FlashMed antigo (até 06/10/2026): id "prova:índice" → chave da mesma questão aqui
    migra = {}
    sa = os.path.join(RAIZ, "docs", "simulados_antigos.json")
    if os.path.exists(sa):
        presentes = {chave_q(q) for q in banco}
        for sim in json.load(open(sa, encoding="utf-8")):
            for x in sim["questions"]:
                k = chave_q(x)
                if k in presentes: migra[x["id"]] = k
    with open(os.path.join(RAIZ, "migra.js"), "w", encoding="utf-8") as f:
        f.write("/* GERADO por monta_banco.py: id da questão no FlashMed antigo → chave no banco novo (usado uma vez por conta, em nuvem.js). */\n")
        f.write("window.MIGRA=" + json.dumps(migra, separators=(",", ":")) + ";\n")
    print(f"migra.js: {len(migra)} questões do FlashMed antigo têm par no banco novo\n")

    r = subprocess.run([sys.executable, os.path.join(RAIZ, "valida_banco.py")])
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
