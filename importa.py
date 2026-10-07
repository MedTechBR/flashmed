#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa as questões dos outros apps de estudo do MedTech para o FlashMed.

O FlashMed junta, num banco só para ENARE/ENAMED:
  - ClínicaMed  (~/Documents/Claude/clinicamed/banco.js)   → Clínica Médica (+ SUS e psiquiatria reclassificados)
  - CirurgiaMed (~/Documents/Claude/cirurgiamed/banco.js)  → Cirurgia Geral
  - RadioTítulo (~/Documents/Claude/radio-titulo/banco.js) → Radiologia (aprofundamento); SÓ as autorais sem
    imagem: o repo de lá é privado, as questões do CBR não são de caderno público e as imagens têm licença NC.

Os bancos de origem continuam sendo a fonte da verdade dessas questões. Rodar de novo atualiza as cópias:
    python3 importa.py && python3 monta_banco.py

Gera:
  lotes-questoes/leva001-imp-clinicamed.json, leva002-imp-cirurgiamed.json, leva003-imp-radiologia.json
  docs/ordem.json   chave → {ex, n}: a que prova real e a que número do caderno cada questão pertence
                    (usado para normalizar `fonte` e montar as provas na íntegra)
"""
import json, os, re, sys, glob
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ); sys.path.insert(0, os.path.join(RAIZ, "docs"))
from valida_banco import chave_q, normtxt
from exames import ORIGEM, EXAMES

C = os.path.expanduser("~/Documents/Claude/")

def le_banco(caminho):
    t = open(caminho, encoding="utf-8").read()
    i = t.index("["); j = t.rindex("]")
    return json.loads(t[i:j+1])

# ---------- mapa de temas ----------
MAPA_CIR = {"bases":"periop","periop":"periop","complic":"periop","infeccao":"periop","critico":"periop",
            "trauma":"trauma","tronco":"trauma","queimados":"trauma","abdome":"abdome","hernias":"hernias",
            "esofago":"digestivo","intestino":"digestivo","hemorragia":"digestivo","hepatobiliar":"hepatobiliar",
            "pancreas":"hepatobiliar","endocrina":"cabeca","onco":"cironco","especialidades":"especialidades",
            "etica":"etica"}
NOME_RADIO = {"torax":"Tórax","neuro":"Neurorradiologia","pediatria":"Pediatria","urogenital":"Urogenital",
              "msk":"Musculoesquelético","mama":"Mama","fisica":"Física, contraste e segurança","usg":"Ultrassonografia e Doppler",
              "digestorio":"Abdome e digestório","seguranca":"Física, contraste e segurança","contraste":"Física, contraste e segurança",
              "densitometria":"Densitometria","usgo":"Ultrassonografia obstétrica e ginecológica","doppler":"Ultrassonografia e Doppler",
              "cabeca_pescoco":"Cabeça e pescoço","intervencao":"Intervenção"}

# Reclassificação das questões de SUS e de psiquiatria do ClínicaMed (que lá são uma área só cada).
# docs/reclass.json = {chave: tema}; o que não estiver lá cai na heurística abaixo.
RECLASS = {}
p = os.path.join(RAIZ, "docs", "reclass.json")
if os.path.exists(p): RECLASS = json.load(open(p, encoding="utf-8"))

def heur_sus(q):
    t = normtxt(q["q"] + " " + " ".join(q["alts"]))
    regras = [("etica", r"etica|sigilo|prontuario|atestado|declaracaodeobito|cfm|bioetic|autonomia|consentimento|testemunhadejeova"),
              ("bioestat", r"sensibilidade|especificidade|valorpreditivo|riscorelativo|oddsratio|ensaioclinico|coorte|casocontrole|metanalise|vies|intervalodeconfianca|nnt|numeronecessario"),
              ("epidemio", r"incidencia|prevalencia|letalidade|mortalidade|indicador|transicao"),
              ("vigilancia", r"notifica|vigilancia|surto|vacina|imuniza|calendario"),
              ("rastreamento", r"rastreamento|rastrear|prevencaoquaternaria|mamografia|citologia|colonoscopia|sangueoculto"),
              ("trabalho", r"trabalhador|ocupacional|cat\b|acidentedetrabalho|materialbiologico"),
              ("aps", r"atencaoprimaria|saudedafamilia|equipe|nasf|emulti|agentecomunitario|territorio|ubs"),
              ("sus", r"lei8080|lei8142|8080|8142|sus|conselho|conferencia|financiamento|regionaliza|integralidade|equidade|universalidade")]
    for tema, rx in regras:
        if re.search(rx, t): return tema
    return "cronicas"

def heur_psiq(q):
    t = normtxt(q["q"] + " " + " ".join(q["alts"]))
    regras = [("drogas", r"alcool|etilis|abstinencia|cocaina|crack|opioide|tabag|nicotina|wernicke|benzodiazepinicodependencia"),
              ("emergpsiq", r"suicid|agitacao|agitado|neurolepticamaligna|serotoninergica|delirium"),
              ("psicoses", r"esquizofren|psicos|alucina|delirio|bipolar|mania|litio|antipsicotic|clozapina|haloperidol"),
              ("psiqinf", r"tdah|autis|anorexia|bulimia|personalidade|insonia"),
              ("raps", r"caps|raps|10216|involuntaria|matriciamento")]
    for tema, rx in regras:
        if re.search(rx, t): return tema
    return "humor"

def limpa(q, extra):
    o = {k: q[k] for k in ("q","alts","gab","tema","sub","cenario","comp","nivel","base","coment","porAlt","fonte","img","imgAlt") if k in q}
    o.update(extra)
    return o

def main():
    vistos = set()
    saida = {}

    # ----- ClínicaMed -----
    cm = le_banco(C + "clinicamed/banco.js"); out = []; recl = {"sus":0,"psiq":0}
    for q in cm:
        k = chave_q(q)
        if k in vistos: continue
        vistos.add(k)
        tema = q["tema"]
        if tema in ("sus", "psiq"):
            tema = RECLASS.get(k) or (heur_sus(q) if tema == "sus" else heur_psiq(q)); recl[q["tema"]] += 1
        out.append(limpa(q, {"tema": tema, "orig": "clinicamed"}))
    saida["leva001-imp-clinicamed.json"] = out
    print(f"ClínicaMed: {len(out)} questões ({recl['sus']} de SUS e {recl['psiq']} de psiquiatria reclassificadas)")

    # ----- CirurgiaMed -----
    out = []
    if os.path.exists(C + "cirurgiamed/banco.js"):
        for q in le_banco(C + "cirurgiamed/banco.js"):
            k = chave_q(q)
            if k in vistos: continue
            vistos.add(k)
            tema = MAPA_CIR.get(q["tema"])
            if not tema: print("  tema de cirurgia sem mapa:", q["tema"]); continue
            o = limpa(q, {"tema": tema, "orig": "cirurgiamed"})
            if q["tema"] in ("bases","complic","infeccao","critico","queimados","tronco","esofago","intestino","hemorragia","pancreas") and not o.get("sub"):
                o["sub"] = q["tema"]
            if o.get("cenario") == "cc" and tema == "etica": o["cenario"] = "amb"
            if len(o["alts"]) == 4 and not o.get("fonte"): pass   # COTECIG tem 4 alternativas: mantém
            out.append(o)
    saida["leva002-imp-cirurgiamed.json"] = out
    print(f"CirurgiaMed: {len(out)} questões")

    # ----- RadioTítulo (só autorais sem imagem) -----
    out = []
    for q in le_banco(C + "radio-titulo/banco.js"):
        if q.get("fonte") or q.get("img"): continue
        k = chave_q(q)
        if k in vistos: continue
        vistos.add(k)
        sub = NOME_RADIO.get(q["tema"], q["tema"])
        o = {"q": q["q"], "alts": q["alts"], "gab": q["gab"], "tema": "radiologia",
             "sub": sub + (" · " + q["sub"] if q.get("sub") else ""),
             "cenario": "amb", "comp": "dx", "nivel": "tit",
             "base": "Banco autoral de radiologia do MedTech (RadioTítulo), revisão 2026",
             "coment": q["coment"], "porAlt": q["porAlt"], "orig": "radiotitulo"}
        out.append(o)
    saida["leva003-imp-radiologia.json"] = out
    print(f"RadioTítulo: {len(out)} questões autorais sem imagem")

    for nome, lista in saida.items():
        with open(os.path.join(RAIZ, "lotes-questoes", nome), "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=1)

    # ----- índice chave → prova real (ex, n) -----
    ordem = {}
    def reg(q, pre, n):
        ex = ORIGEM.get(pre)
        if not ex: return
        for k in (chave_q(q), "p:" + normtxt(q["q"])[:150]):
            ordem.setdefault(k, {"ex": ex, **({"n": n} if n else {})})
    cand = json.load(open(C + "clinicamed/provas-reais/candidatas.json", encoding="utf-8"))
    for x in cand:
        pre, n = x["id"].split("#"); reg(x, pre, int(n))
    cc = C + "cirurgiamed/provas-reais/cand_cir.json"
    if os.path.exists(cc):
        for x in json.load(open(cc, encoding="utf-8")):
            m = re.match(r"(en2[45]-cg|usp2[56]-cir|usp2[56]-cad)-(\d+)$", x["id"])
            if m: reg(x, m.group(1), int(m.group(2)))
            m = re.match(r"cm-(rev\d{4}(?:_\d)?_pv)-(\d+)$", x["id"])
            if m: reg(x, m.group(1), int(m.group(2)))
    sims = os.path.join(RAIZ, "docs", "simulados_antigos.json")
    if os.path.exists(sims):
        for s in json.load(open(sims, encoding="utf-8")):
            for i, x in enumerate(s["questions"]):
                reg({"q": x["q"]}, s["id"], None)
    json.dump(ordem, open(os.path.join(RAIZ, "docs", "ordem.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"docs/ordem.json: {len(ordem)//2} questões de prova indexadas")

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------
# Cartões: flash.js do ClínicaMed e do CirurgiaMed (tema remapeado) + docs/flash_*.json do FlashMed
# ---------------------------------------------------------------------------------------------
def importa_flash():
    import subprocess
    def le(caminho):
        out = subprocess.run(["node", "-e", f"global.window={{}};require({json.dumps(caminho)});console.log(JSON.stringify(window.FLASH||[]))"],
                             capture_output=True, text=True, check=True).stdout
        return json.loads(out)
    tax = re.findall(r'"id":"(\w+)","grande"', open(os.path.join(RAIZ, "taxonomia.js"), encoding="utf-8").read())
    cards, vistos = [], set()
    def poe(c, tema, orig):
        if tema not in tax: return
        k = normtxt(c["a"])
        if k in vistos: return
        vistos.add(k); cards.append({"tema": tema, "a": c["a"], "b": c["b"], "orig": orig})
    MAPA_CM = {"sus": "sus", "psiq": "humor"}
    for c in le(C + "clinicamed/flash.js"):
        t = c.get("tema"); t = MAPA_CM.get(t, t)
        if c.get("tema") == "sus": t = heur_sus({"q": c["a"] + " " + c["b"], "alts": []})
        if c.get("tema") == "psiq": t = heur_psiq({"q": c["a"] + " " + c["b"], "alts": []})
        poe(c, t, "clinicamed")
    if os.path.exists(C + "cirurgiamed/flash.js"):
        for c in le(C + "cirurgiamed/flash.js"): poe(c, MAPA_CIR.get(c.get("tema"), c.get("tema")), "cirurgiamed")
    for arq in sorted(glob.glob(os.path.join(RAIZ, "docs", "flash_*.json"))):
        for c in json.load(open(arq, encoding="utf-8")): poe(c, c.get("tema"), "flashmed")
    with open(os.path.join(RAIZ, "flash.js"), "w", encoding="utf-8") as f:
        f.write("/* GERADO por importa.py: cartões do ClínicaMed, do CirurgiaMed e os próprios do FlashMed (docs/flash_*.json).\n"
                "   `a` é a frente, `b` o verso, `tema` a subárea. O verso traz o número e a fonte com ano. */\n")
        f.write("window.FLASH=" + json.dumps(cards, ensure_ascii=False, indent=0) + ";\n")
    from collections import Counter
    print(f"flash.js: {len(cards)} cartões", dict(Counter(c['orig'] for c in cards)))

if __name__ == "__main__":
    importa_flash()
