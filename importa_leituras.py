#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa as leituras do ClínicaMed e do CirurgiaMed para o FlashMed e monta leituras.js.

Cada app de origem vai para uma subpasta própria (leituras/cm/, leituras/cir/) com a sua pasta fig/,
para que os links entre leituras (href="x.html#ancora") e as figuras (fig/...) continuem valendo sem
reescrever o HTML. Só três coisas mudam na cópia:
  - _leitura.css/_leitura.js apontam para a pasta de cima (um só par para o app inteiro);
  - o botão "treinar questões" volta dois níveis (../../index.html) e usa o tema do FlashMed;
  - nada mais. O texto é o do app de origem: corrigir lá e rodar isto de novo.

As leituras próprias do FlashMed ficam na raiz de leituras/ e entram pelo índice
leituras/_entradas_*.json (escritas pelos redatores). leituras.js é GERADO aqui:
    python3 importa_leituras.py && python3 gera_indice.py
"""
import json, os, re, shutil, subprocess, glob
RAIZ = os.path.dirname(os.path.abspath(__file__))
C = os.path.expanduser("~/Documents/Claude/")
L = os.path.join(RAIZ, "leituras")

# tema do app de origem → subárea do FlashMed (só onde muda)
MAPA_AREA = {"cm": {"sus": "sus", "psiq": "humor"},
             "cir": {"bases":"periop","periop":"periop","complic":"periop","infeccao":"periop","critico":"periop",
                     "trauma":"trauma","tronco":"trauma","queimados":"trauma","esofago":"digestivo","intestino":"digestivo",
                     "hemorragia":"digestivo","pancreas":"hepatobiliar","endocrina":"cabeca","onco":"cironco","etica":"etica"}}

def le_leituras_js(caminho):
    """leituras.js dos outros apps é JS com chaves sem aspas: avaliar com node."""
    out = subprocess.run(["node", "-e", f"global.window={{}};require({json.dumps(caminho)});console.log(JSON.stringify(window.LEITURAS))"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def copia(app, pasta_origem):
    dest = os.path.join(L, app)
    if os.path.isdir(dest): shutil.rmtree(dest)
    os.makedirs(dest)
    if os.path.isdir(os.path.join(pasta_origem, "fig")):
        shutil.copytree(os.path.join(pasta_origem, "fig"), os.path.join(dest, "fig"))
    n = 0
    for f in sorted(glob.glob(os.path.join(pasta_origem, "*.html"))):
        s = open(f, encoding="utf-8").read()
        s = re.sub(r'(href|src)="(_leitura\.(?:css|js))(\?v=\d+)?"', lambda m: f'{m.group(1)}="../{m.group(2)}?v=1"', s)
        def treino(m):
            area = MAPA_AREA.get(app, {}).get(m.group(1), m.group(1))
            return f'href="../../index.html?area={area}#questoes"'
        s = re.sub(r'href="\.\./index\.html\?area=([a-z_]+)#questoes"', treino, s)
        open(os.path.join(dest, os.path.basename(f)), "w", encoding="utf-8").write(s)
        n += 1
    return n

def main():
    itens = []
    # ---------- próprias do FlashMed (raiz de leituras/) ----------
    proprias = []
    for arq in sorted(glob.glob(os.path.join(L, "_entradas_*.json"))):
        proprias.extend(json.load(open(arq, encoding="utf-8")))
    ordem_grupo = ["Ginecologia e Obstetrícia", "Pediatria", "Medicina de Família e Comunidade",
                   "Saúde Coletiva e SUS", "Saúde Mental"]
    grupos = {}
    for e in proprias:
        if not os.path.exists(os.path.join(L, e["f"])): print("  sem arquivo:", e["f"]); continue
        grupos.setdefault(e.get("grupo", "Outras"), []).append({k: v for k, v in e.items() if k != "grupo"})
    for g in ordem_grupo + sorted(set(grupos) - set(ordem_grupo)):
        if g in grupos:
            itens.append({"grupo": g, "sub": "", "orig": "flashmed"})
            itens.extend(grupos[g])
    print(f"FlashMed: {sum(len(v) for v in grupos.values())} leituras próprias")

    # ---------- ClínicaMed e CirurgiaMed ----------
    for app, pasta, nome in (("cm", C + "clinicamed", "Clínica Médica (do ClínicaMed)"),
                             ("cir", C + "cirurgiamed", "Cirurgia (do CirurgiaMed)")):
        if not os.path.exists(os.path.join(pasta, "leituras.js")): continue
        n = copia(app, os.path.join(pasta, "leituras"))
        lst = le_leituras_js(os.path.join(pasta, "leituras.js"))
        presentes = set(os.listdir(os.path.join(L, app)))
        k = 0
        for e in lst:
            if "grupo" in e:
                itens.append({"grupo": e["grupo"], "sub": e.get("sub", ""), "orig": app}); continue
            if e.get("f") not in presentes: continue
            e = dict(e); e["f"] = f"{app}/{e['f']}"
            e["area"] = MAPA_AREA.get(app, {}).get(e.get("area"), e.get("area"))
            itens.append(e); k += 1
        print(f"{nome}: {n} arquivos copiados, {k} no índice")
    # remove grupos vazios
    limpo = []
    for i, e in enumerate(itens):
        if "grupo" in e and (i + 1 >= len(itens) or "grupo" in itens[i + 1]): continue
        limpo.append(e)
    with open(os.path.join(RAIZ, "leituras.js"), "w", encoding="utf-8") as f:
        f.write("/* GERADO por importa_leituras.py: leituras próprias do FlashMed (leituras/*.html) e as importadas\n"
                "   do ClínicaMed (leituras/cm/) e do CirurgiaMed (leituras/cir/). `area` é a subárea (taxonomia.js);\n"
                "   `orig` no grupo diz de que app vieram. Não editar à mão. */\n")
        f.write("window.LEITURAS=" + json.dumps(limpo, ensure_ascii=False, indent=0) + ";\n")
    print(f"leituras.js: {sum(1 for e in limpo if 'f' in e)} leituras")

if __name__ == "__main__":
    main()
