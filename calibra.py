#!/usr/bin/env python3
"""Mantém as alternativas na janela de 95–108% do comprimento da correta.

Duas funções:
  ajusta(arq, qi, {prefixo: [variantes]}, nova_correta=[...])  — escolhe a variante que cabe
  encaixa_todas(arq)  — passa o banco inteiro e ajusta por SUFIXO NEUTRO o que estiver curto

Existe porque toda reescrita de alternativa reabre o viés de comprimento e acertar no olho custa
uma ida e volta por tentativa. Os sufixos são deliberadamente neutros: não mudam o motivo pelo qual
a alternativa está certa ou errada, só o tamanho.
"""
import json, glob, re

SUFIXOS = ["", " agora", " neste caso", " nesse contexto", " para este paciente", " na avaliação inicial",
           " desde o primeiro momento", " ao longo do seguimento", " durante a internação",
           " conforme o quadro apresentado", " diante do quadro descrito acima",
           " conforme o quadro clínico apresentado por ele", " diante do quadro clínico descrito no enunciado",
           " conforme a gravidade e a resposta clínica observada", " tanto na fase inicial quanto no seguimento"]

def _janela(q):
    Lc = len(q["alts"][q["gab"]])
    return Lc * 0.95, Lc * 1.08

def ajusta(arq, qi, mapa, nova_correta=None):
    b = json.load(open(arq, encoding="utf-8")); q = b[qi]
    if nova_correta:
        outras = [len(a) for i, a in enumerate(q["alts"]) if i != q["gab"]]
        lo, hi = max(outras) / 1.08, min(outras) / 0.95
        ok = [c for c in nova_correta if lo <= len(c) <= hi]
        if ok: q["alts"][q["gab"]] = ok[0]
        else: print(f"  correta: janela {round(lo)}-{round(hi)}, candidatas {[len(c) for c in nova_correta]}")
    lo, hi = _janela(q)
    for i, a in enumerate(q["alts"]):
        for pref, variantes in mapa.items():
            if not a.startswith(pref): continue
            ok = [v for v in variantes if lo <= len(v) <= hi]
            if ok: q["alts"][i] = ok[0]
            else: print(f"  alt{i}: janela {round(lo)}-{round(hi)}, candidatas {[len(v) for v in variantes]}")
    json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def _com_sufixo(txt, lo, hi):
    """Acrescenta um complemento neutro até o texto caber na janela. Devolve None se não couber."""
    base = txt.rstrip(".")
    for s in SUFIXOS:
        cand = base + s + "."
        if lo <= len(cand) <= hi: return cand
    return None

def encaixa_todas(padrao="lotes-questoes/leva*.json", verboso=True):
    """Ajusta por sufixo neutro toda alternativa CURTA demais. Alternativa longa demais não é
    tocada — encurtar automaticamente arriscaria cortar o que a torna errada."""
    ajustadas = pendentes = 0
    for arq in sorted(glob.glob(padrao)):
        b = json.load(open(arq, encoding="utf-8")); mudou = False
        for qi, q in enumerate(b):
            if len(q.get("alts", [])) != 5: continue
            lo, hi = _janela(q)
            for i, a in enumerate(q["alts"]):
                if i == q["gab"] or lo <= len(a) <= hi: continue
                if len(a) < lo:
                    novo = _com_sufixo(a, lo, hi)
                    if novo: q["alts"][i] = novo; ajustadas += 1; mudou = True
                    else: pendentes += 1; print(f"  {arq.split('/')[-1]} q{qi} alt{i}: curta ({len(a)}), janela {round(lo)}-{round(hi)}")
                else:
                    # alternativa longa demais: pela regra do projeto, alonga-se a CORRETA em vez de
                    # encurtar o distrator (encurtar arrisca cortar justamente o que o torna errado)
                    outras = [len(x) for k, x in enumerate(q["alts"]) if k != q["gab"]]
                    alvo_lo, alvo_hi = max(outras) / 1.08, min(outras) / 0.95
                    nova = _com_sufixo(q["alts"][q["gab"]], alvo_lo, alvo_hi) if alvo_lo <= alvo_hi else None
                    if nova:
                        q["alts"][q["gab"]] = nova; ajustadas += 1; mudou = True
                        lo, hi = _janela(q)
                    else:
                        pendentes += 1
                        if verboso: print(f"  {arq.split('/')[-1]} q{qi} alt{i}: LONGA ({len(a)}), janela {round(lo)}-{round(hi)} — ajustar à mão")
        if mudou: json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{ajustadas} alternativas encaixadas por sufixo; {pendentes} pendentes")
    return pendentes



# --- tell visual: distrator longo sem NENHUM acento ao lado de correta acentuada ---
# do menor ao maior: quase sempre basta um "já" para o texto deixar de ser visualmente "liso"
SUF_ACENTO = [" já", " após isso", " já de saída", " nesse contexto clínico", " já na avaliação inicial",
              " após a estabilização", " já no primeiro atendimento", " em caráter de urgência"]
_ACENTO = re.compile(r"[àáâãéêíóôõúç]", re.I)
A_ABS = re.compile(r"\b(sempre|nunca|jamais|apenas|somente|exclusivamente|tod[oa]s?|nenhum[a]?|qualquer|quaisquer|invariavelmente)\b", re.I)

def acentua_distratores(padrao="lotes-questoes/leva*.json"):
    """Acrescenta um complemento ACENTUADO e neutro a distratores longos que não têm nenhum acento,
    quando a correta tem — o tell é visual: a alternativa 'lisa' se destaca no meio das outras."""
    n = pend = 0
    for arq in sorted(glob.glob(padrao)):
        b = json.load(open(arq, encoding="utf-8")); mudou = False
        for qi, q in enumerate(b):
            if len(q.get("alts", [])) != 5: continue
            g = q["gab"]
            if not _ACENTO.search(q["alts"][g]): continue
            lo, hi = _janela(q)
            for i, a in enumerate(q["alts"]):
                if i == g or len(a) <= 60 or _ACENTO.search(a): continue
                base = a.rstrip(".")
                cands = [base + suf + "." for suf in SUF_ACENTO]
                # inserir "já " depois da primeira vírgula costuma soar mais natural que sufixo no fim
                if ", " in a: cands.insert(0, a.replace(", ", ", já ", 1))
                for cand in cands:
                    if lo <= len(cand) <= hi and _ACENTO.search(cand):
                        q["alts"][i] = cand; n += 1; mudou = True; break
                else:
                    pend += 1
                    print(f"  {arq.split('/')[-1]} q{qi} alt{i}: sem acento, não coube sufixo (janela {round(lo)}-{round(hi)})")
        if mudou: json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{n} distratores acentuados; {pend} pendentes")
    return pend



# --- tell: termos absolutos concentrados nos distratores, com a correta "limpa" ---
# O sufixo é tautológico de propósito: se a alternativa é a conduta certa PARA O CASO DESCRITO,
# dizer que vale "em qualquer caso semelhante" não muda o conteúdo clínico — só tira da correta a
# marca de ser a única sem absoluto, que é o que o aluno aprende a explorar.
SUF_ABS = [" sempre", " em todo caso", " sempre nesse caso", " em qualquer caso assim",
           " em todo caso semelhante", " em qualquer caso semelhante",
           " sempre que o quadro for esse", " em todos os casos semelhantes a este"]

def desmarca_correta(padrao="lotes-questoes/leva*.json", limiar=3):
    n = pend = 0
    for arq in sorted(glob.glob(padrao)):
        b = json.load(open(arq, encoding="utf-8")); mudou = False
        for qi, q in enumerate(b):
            if len(q.get("alts", [])) != 5: continue
            g = q["gab"]
            if A_ABS.search(q["alts"][g]): continue
            if sum(1 for j, a in enumerate(q["alts"]) if j != g and A_ABS.search(a)) < limiar: continue
            outras = [len(a) for j, a in enumerate(q["alts"]) if j != g]
            lo, hi = max(outras) / 1.08, min(outras) / 0.95
            base = q["alts"][g].rstrip(".")
            cands = [base + suf + "." for suf in SUF_ABS]
            if ", " in q["alts"][g]:   # "sempre" no meio soa melhor que no fim
                cands.insert(0, q["alts"][g].replace(", ", ", sempre ", 1))
            for cand in cands:
                if lo <= len(cand) <= hi:
                    q["alts"][g] = cand; n += 1; mudou = True; break
            else:
                pend += 1
                print(f"  {arq.split('/')[-1]} q{qi}: correta sem absoluto (janela {round(lo)}-{round(hi)}, correta {len(q['alts'][g])})")
        if mudou: json.dump(b, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{n} corretas desmarcadas; {pend} pendentes")
    return pend

if __name__ == "__main__":
    encaixa_todas()
    acentua_distratores()
    desmarca_correta()
    encaixa_todas(verboso=False)
