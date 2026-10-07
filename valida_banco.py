#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validador do banco do FlashMed (fork do validador do ClínicaMed).   Uso: python3 valida_banco.py
Sai com código 1 se houver erro DURO. Avisos não derrubam o build.

Herda as defesas do TráfegoTítulo/RadioTítulo e acrescenta o que é próprio daqui:
  - as TRÊS matrizes do edital (especialidade, cenário, competência) são obrigatórias
  - `base` precisa citar diretriz E ano (rigor clínico: conduta envelhece)
  - `nivel` situa a questão entre R1 e título
  - alvo de cobertura por área é PROPORCIONAL ao peso na prova de 120 questões
"""
import json, os, re, sys, unicodedata, statistics

RAIZ = os.path.dirname(os.path.abspath(__file__))
ALVO_POR_PESO = 12         # 12 questões por ponto de peso numa prova de 100 → banco "cheio" ≈ 1.200 no formato da prova

def carrega_js(nome, var):
    txt = open(os.path.join(RAIZ, nome), encoding="utf-8").read()
    m = re.search(r"window\." + var + r"\s*=\s*(\[.*?\])\s*;", txt, re.S)
    if not m:
        print(f"ERRO DURO: não achei window.{var} em {nome}"); sys.exit(1)
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        print(f"ERRO DURO: {nome} não é JSON estrito: {e}"); sys.exit(1)

def normtxt(s):
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if not ("̀" <= c <= "ͯ"))
    return re.sub(r"[^a-z0-9]", "", s.lower())

def b36(n):
    if n == 0: return "0"
    dig = "0123456789abcdefghijklmnopqrstuvwxyz"; out = ""
    while n: out = dig[n % 36] + out; n //= 36
    return out

def chave_q(q):
    """Réplica exata do chaveQ do app (djb2 + FNV com Math.imul)."""
    t = normtxt(q.get("q", ""))
    h1, h2 = 5381, 0x811C9DC5
    for ch in t:
        c = ord(ch)
        h1 = ((h1 << 5) + h1 + c) & 0xFFFFFFFF
        h2 = ((h2 ^ c) * 0x01000193) & 0xFFFFFFFF
    return (b36(h1) + b36(h2))[:10]

# "toda/todas/qualquer" são tão absolutos quanto "todo/todos" e faltavam aqui: a regex herdada
# via só o masculino e deixava passar o tell em um terço do banco.
ABSOLUTOS = re.compile(r"\b(sempre|nunca|jamais|apenas|somente|exclusivamente|tod[oa]s?|nenhum[a]?|qualquer|quaisquer|invariavelmente)\b", re.I)
CAUTELA   = re.compile(r"\b(pode(m)?|geralmente|costuma(m)?|tende(m)?|recomenda-se|habitualmente|em geral)\b", re.I)
PREFIXO   = re.compile(r"^\s*[A-Ea-e][\)\.\-–]\s")
ANO       = re.compile(r"\b(19|20)\d{2}\b")

def main():
    banco = carrega_js("banco.js", "BANCO")
    tax   = carrega_js("taxonomia.js", "TAXONOMIA")
    cen   = {c["id"] for c in carrega_js("taxonomia.js", "CENARIOS")}
    comp  = {c["id"] for c in carrega_js("taxonomia.js", "COMPETENCIAS")}
    niv   = {n["id"] for n in carrega_js("taxonomia.js", "NIVEIS")}
    temas = {t["id"] for t in tax}
    duros, avisos = [], []
    chaves = {}
    correta_mais_longa = 0
    reais_total = 0
    reais_correta_mais_longa = 0
    folgas, dist_gab = [], {}
    por_tema  = {t["id"]: 0 for t in tax}
    por_cen   = {c: 0 for c in cen}
    por_comp  = {c: 0 for c in comp}
    por_niv   = {c: 0 for c in niv}

    for i, q in enumerate(banco):
        rot = f"Q{i+1}"
        faltou = False
        for campo in ("q", "alts", "gab", "tema", "coment", "cenario", "comp", "nivel", "base"):
            if campo not in q:
                duros.append(f"{rot}: falta campo '{campo}'"); faltou = True; break
        if faltou: continue

        alts, gab = q["alts"], q["gab"]
        # Questao de prova REAL (tem `fonte`) pode ter 4 alternativas — Revalida e ENARE usam 4.
        # Questao autoral segue o formato da prova TECM, com 5.
        real = isinstance(q.get("fonte"), dict)
        # Importadas do CirurgiaMed (formato COTECIG) e do RadioTítulo têm 4 alternativas por desenho.
        permitidos = (4, 5) if (real or q.get("orig") in ("cirurgiamed", "radiotitulo")) else (5,)
        if not isinstance(alts, list) or len(alts) not in permitidos:
            esperado = "4 ou 5 (prova real ou importada)" if real else "5 (autoral)"
            duros.append(f"{rot}: esperado {esperado} alternativas — achei {len(alts) if isinstance(alts,list) else '?'}"); continue
        if not isinstance(gab, int) or not (0 <= gab < len(alts)):
            duros.append(f"{rot}: gab fora do range"); continue
        if q.get("orig") not in (None, "clinicamed", "cirurgiamed", "radiotitulo", "flashmed"):
            duros.append(f"{rot}: orig desconhecida {q.get('orig')!r}")
        if q["tema"] not in temas:   duros.append(f"{rot}: tema '{q['tema']}' não existe na taxonomia")
        if q["cenario"] not in cen:  duros.append(f"{rot}: cenario '{q['cenario']}' fora da matriz do edital ({sorted(cen)})")
        if q["comp"] not in comp:    duros.append(f"{rot}: comp '{q['comp']}' fora da matriz do edital ({sorted(comp)})")
        if q["nivel"] not in niv:    duros.append(f"{rot}: nivel '{q['nivel']}' inválido ({sorted(niv)})")
        if len(q.get("coment", "")) < 150:
            duros.append(f"{rot}: comentário ausente/curto (<150 chars) — obrigatório em TODAS")
        pa = q.get("porAlt")
        if not (isinstance(pa, list) and len(pa) == len(alts) and all(len(x) > 20 for x in pa)):
            duros.append(f"{rot}: porAlt ausente/incompleto (1 explicação por alternativa)")
        # rigor clínico: a âncora precisa de diretriz E ano
        b = q.get("base", "")
        if len(b) < 12:
            duros.append(f"{rot}: 'base' curta — cite a diretriz/sociedade que ancora a conduta")
        elif not ANO.search(b):
            duros.append(f"{rot}: 'base' sem ANO ({b!r}) — conduta clínica envelhece; a versão da diretriz é obrigatória")
        ch = chave_q(q)
        if ch in chaves: duros.append(f"{rot}: colisão de chave com {chaves[ch]} (enunciado igual/quase igual)")
        chaves[ch] = rot
        f = q.get("fonte")
        if f is not None and not (isinstance(f, dict) and f.get("banca") and f.get("ano")):
            duros.append(f"{rot}: fonte presente mas sem banca+ano")

        norms = [" ".join(a.lower().split()) for a in alts]   # sem normtxt: "D1" e "D1+" são alternativas diferentes
        if len(set(norms)) != len(norms): duros.append(f"{rot}: alternativas duplicadas")
        for j, a in enumerate(alts):
            if PREFIXO.match(a): duros.append(f"{rot} alt {j}: prefixo de letra dentro do texto")
        Lc = len(alts[gab])
        outras = [len(a) for j, a in enumerate(alts) if j != gab]

        # ---------------------------------------------------------------
        # As regras abaixo (comprimento, termos absolutos, cautela, acento)
        # policiam vicio de ESCRITA AUTORAL. Elas NAO se aplicam a questao de
        # prova real: o texto da banca e um fato historico, e reescrever uma
        # alternativa oficial para caber em 95-108% falsificaria a questao e
        # destruiria justamente o que a torna util — treinar no enunciado que
        # a banca escreveu, com os tells que a banca teve. O vies de tamanho
        # das questoes reais e medido e reportado, nao corrigido.
        # ---------------------------------------------------------------
        # A faixa de 95-108% foi ABANDONADA em 09/09/2026: aferida contra as 211 questões de banca
        # do próprio banco, ela reprovava 79% das alternativas oficiais (razão distrator/correta:
        # mediana 100%, mas p5 de 53% e p95 de 194%). Uniformizar comprimento é falsa precisão — e
        # foi ela que produziu as alternativas longas, explicativas e todas do mesmo tamanho que
        # deixaram as questões fáceis. O que importa é medido por LOTE em docs/audita_questoes.py:
        # a correta não pode ser a mais longa muito acima do acaso. Aqui fica só o extremo, que é
        # tell de verdade: distrator curto demais ao lado de uma correta longa entrega a resposta.
        if not real:
            for j, a in enumerate(alts):
                r = len(a) / Lc
                if r < 0.45 or r > 2.4:
                    duros.append(f"{rot} alt {j}: comprimento {len(a)} = {r*100:.0f}% da correta ({Lc}) — fora de 45–240%")
        if Lc > max(outras):
            correta_mais_longa += 1
            folgas.append((Lc - max(outras)) / max(outras) * 100)
            if real: reais_correta_mais_longa += 1
        if real: reais_total += 1

        # Limiar 3, não 2: medido no banco de 107 questões, o padrão "2 distratores com absoluto e
        # correta sem" ocorre em 23 questões mas ainda deixa 2 outras alternativas sem absoluto —
        # marcar "a que não tem absoluto" não resolve a questão. O tell só fica explorável a partir
        # de 3 distratores, quando sobra praticamente uma escolha. Distrator errado POR restringir
        # demais ("tratar apenas com X") é conteúdo, não vício de escrita.
        abs_err = sum(1 for j, a in enumerate(alts) if j != gab and ABSOLUTOS.search(a))
        if not real and abs_err >= 3 and not ABSOLUTOS.search(alts[gab]):
            avisos.append(f"{rot}: termos absolutos concentrados nos distratores ({abs_err} de 4)")
        if not real and CAUTELA.search(alts[gab]) and not any(CAUTELA.search(a) for j, a in enumerate(alts) if j != gab):
            avisos.append(f"{rot}: linguagem cautelosa só na correta")
        tem_acento = lambda s: bool(re.search(r"[àáâãéêíóôõúç]", s, re.I))
        if not real and tem_acento(alts[gab]):
            for j, a in enumerate(alts):
                if j != gab and len(a) > 60 and not tem_acento(a):
                    avisos.append(f"{rot} alt {j}: distrator longo sem nenhum acento (tell visual)")

        dist_gab[gab] = dist_gab.get(gab, 0) + 1
        por_tema[q["tema"]] = por_tema.get(q["tema"], 0) + 1
        por_cen[q["cenario"]]  = por_cen.get(q["cenario"], 0) + 1
        por_comp[q["comp"]]    = por_comp.get(q["comp"], 0) + 1
        por_niv[q["nivel"]]    = por_niv.get(q["nivel"], 0) + 1

    n = len(banco)
    print(f"— Banco: {n} questões | chaves únicas: {len(chaves)}")
    if n:
        pct = correta_mais_longa / n * 100
        print(f"— Correta é a mais longa: {correta_mais_longa}/{n} = {pct:.1f}% (após igualar tamanhos, ~55% é normal; 80% é o vício de IA)")
        if reais_total:
            aut = n - reais_total
            aut_longa = correta_mais_longa - reais_correta_mais_longa
            print(f"   ↳ autorais: {aut_longa}/{aut} = {aut_longa/aut*100:.1f}%  |  provas reais: "
                  f"{reais_correta_mais_longa}/{reais_total} = {reais_correta_mais_longa/reais_total*100:.1f}% "
                  f"(medido, não corrigido — o texto da banca não se reescreve)")
        if folgas:
            print(f"— Folga da correta sobre a 2ª maior: mediana {statistics.median(folgas):.1f}% | máx {max(folgas):.1f}% (alvo mediana <=6%)")
        print("— Gabarito: " + ", ".join(f"{chr(65+k)}:{v}" for k, v in sorted(dist_gab.items())))
        reais = sum(1 for q in banco if q.get("fonte"))
        print(f"— Procedência: {reais} de prova real, {n - reais} autorais")
        print("— Cenário: "     + ", ".join(f"{k}:{v}" for k, v in sorted(por_cen.items())))
        print("— Competência: " + ", ".join(f"{k}:{v}" for k, v in sorted(por_comp.items())))
        print("— Nível: "       + ", ".join(f"{k}:{v}" for k, v in sorted(por_niv.items())))
    grandes = carrega_js("taxonomia.js", "GRANDES")
    gde = {t["id"]: t["grande"] for t in tax}
    print("— Por grande área: " + ", ".join(f"{g['curto']}:{sum(por_tema[t] for t in por_tema if gde.get(t)==g['id'])}" for g in grandes))
    reais_g = {}
    for q in banco:
        if q.get("fonte"): reais_g[gde.get(q.get("tema"))] = reais_g.get(gde.get(q.get("tema")), 0) + 1
    print("— De prova real por grande área: " + ", ".join(f"{g['curto']}:{reais_g.get(g['id'],0)}" for g in grandes))
    print("— Cobertura por subárea (alvo = peso na prova × 12):")
    for t in sorted(tax, key=lambda x: -x["peso"]):
        c, alvo = por_tema[t["id"]], t["peso"] * ALVO_POR_PESO
        marca = "OK " if c >= alvo else f"faltam {alvo - c}"
        print(f"    {t['nome']:<44} {c:>4}/{alvo:<4} {marca}")
    if avisos:
        print(f"\nAVISOS ({len(avisos)}):")
        for a in avisos: print("  ~", a)
    if duros:
        print(f"\nERROS DUROS ({len(duros)}):")
        for d in duros: print("  !", d)
        sys.exit(1)
    print("\nOK: nenhum erro duro.")

if __name__ == "__main__":
    main()
