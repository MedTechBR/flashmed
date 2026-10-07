#!/usr/bin/env python3
"""Extrai questões VERBATIM dos cadernos oficiais (texto de `pdftotext` sem -layout, em raw/).

Uso: python3 extrai.py <id> <arquivo_raw.txt> <estilo: revalida|enare>
Saída: parsed/<id>.json — lista de {n, q, alts, avisos}.
O texto da banca não é reescrito: só junta linhas quebradas e tira cabeçalho/rodapé de página.

Número de página: só sai o número solto que é a ÚLTIMA linha não vazia da página (o `colunas_pdf.py`
imprime o rodapé por último) e cabe no total de páginas. Até 07/10/2026 o LIXO apagava TODA linha
que fosse só um número, e isso comia dado no meio do texto e das tabelas ("de 55 anos" virou
"de anos"; a célula "PTH 125" sumiu). Número solto no meio da página é conteúdo: fica.
"""
import json, re, sys, pathlib

LIXO = [
    r"^ÁREA LIVRE$", r"^RASCUNHO$", r"^Página \d+", r".*Página \d+ de \d+",
    r"^Residência Médica$", r"^FGV Conhecimento$", r"^Clínica Médica$", r"^Tipo \d.*Página \d+$",
    r"^Pré-Requisito - .*", r"^Ano Adicional - .*", r"^Acesso Direto.*", r"^\*$", r"^REVALIDA.*", r"^Revalida.*",
    r"^INEP.*", r"^#+$", r"^PRÉ-REQUISITO\b.*", r"^FGV CONHECIMENTO$", r"^Tipo \d - .*", r"^Realização$", r"^Processo Seletivo.*", r"^PROCESSO SELETIVO.*", r".*(PRIMEIRA|SEGUNDA) EDIÇÃO.*", r"^\d{4}\s+.*EDIÇÃO.*", r"^PROVA OBJETIVA.*", r"^CADERNO \d+.*", r"^EDIÇÃO.*",
    r"^TIPO \d+ – PÁGINA \d+$", r"^EXAME NACIONAL DE RESIDÊNCIA$", r"^ÁREA DE ATUAÇÃO .*", r"^ANO ADICIONAL .*", r"^Área de Atuação - .*",
]
LIXO = [re.compile(p) for p in LIXO]

NUM_PAGINA = re.compile(r"^\(?\d{1,3}\)?$")

def tira_numero_de_pagina(texto):
    """Apaga o número de página pela POSIÇÃO e pela SEQUÊNCIA: o número solto que é a última linha não
    vazia da página (separada por \\f) E segue a numeração do próprio caderno (índice da página +
    deslocamento constante, visto em pelo menos 3 páginas). Caderno sem número de página (Revalida
    2023.2) não perde nada, nem uma célula de tabela que por acaso feche a página."""
    import collections
    paginas = [pg.split("\n") for pg in texto.split("\f")]
    ultima = {}
    for ip, ls in enumerate(paginas):
        for i in range(len(ls) - 1, -1, -1):
            s = ls[i].strip()
            if s:
                if NUM_PAGINA.match(s):
                    ultima[ip] = (i, int(s.strip("()")))
                break
    desl = collections.Counter(v - ip for ip, (_, v) in ultima.items())
    if not desl or desl.most_common(1)[0][1] < 3:
        return texto
    d = desl.most_common(1)[0][0]
    for ip, (i, v) in ultima.items():
        if v - ip == d:
            paginas[ip][i] = ""
    return "\f".join("\n".join(ls) for ls in paginas)

def limpa(linhas):
    out = []
    for l in linhas:
        s = l.strip().replace("­", "")
        if not s or any(p.match(s) for p in LIXO):
            continue
        out.append(s)
    return out

def junta(linhas):
    txt = ""
    for s in linhas:
        if not txt:
            txt = s
        elif txt.endswith("-") and not txt.endswith(" -"):
            txt = txt[:-1] + s          # hifenização de fim de linha
        else:
            txt += " " + s
    txt = re.sub(r"\s+", " ", txt).strip()
    txt = re.sub(r" ([,.;:?])", r"\1", txt)
    return txt

def blocos(texto, estilo):
    linhas = texto.split("\n")
    if estilo == "revalida":
        marca = re.compile(r"^QUESTÃO\s+(\d{1,3})\s*$")
    elif estilo == "usp":
        marca = re.compile(r"^\{(\d{1,3})\}$")
    else:
        marca = re.compile(r"^(\d{1,3})$")
    blk, cur, n = {}, None, None
    esperado = 1
    COMP.clear()
    comp_ativo = None
    for l in linhas:
        if "####" in l:
            l = l.split("####")[0]
        mt = re.match(r"^\s*TEXTO PARA AS QUEST(?:ÕES|OES)\s+(?:DE\s+)?(\d+)\s+(?:E|A)\s+(\d+)", l, re.I)
        if mt:
            if cur is not None:
                blk.setdefault(n, []).extend(cur)
            cur, n = None, None
            comp_ativo = (int(mt.group(1)), int(mt.group(2)), [])
            COMP.append(comp_ativo)
            continue
        if cur is not None and n and n >= 50 and re.search(r"QUESTIONÁRIO DE PERCEPÇÃO|Questionário de Percepção", l):
            break
        m = marca.match(l.strip())
        if m:
            k = int(m.group(1))
            # no ENARE o número solto também aparece em rodapé: só aceita o próximo esperado
            if estilo == "enare" and k != esperado:
                if cur is not None:
                    cur.append(l)
                continue
            if cur is not None:
                blk.setdefault(n, []).extend(cur)
            n, cur = k, []
            esperado = k + 1
            comp_ativo = None
            continue
        if comp_ativo is not None:
            comp_ativo[2].append(l)
        elif cur is not None:
            cur.append(l)
    if cur is not None:
        blk.setdefault(n, []).extend(cur)
    return blk

_ALT = re.compile(r"^\(([A-E])\)\s*(.*)$|^([A-E])\s+(.*)$")
class _M:
    def __init__(s, l, t): s.l, s.t = l, t
    def group(s, i): return s.l if i == 1 else s.t
class ALT:
    @staticmethod
    def match(s):
        m = _ALT.match(s)
        if not m: return None
        return _M(m.group(1) or m.group(3), m.group(2) if m.group(1) else m.group(4))

NALT = 5
COMP = []

def separa(linhas, estilo):
    ls = limpa(linhas)
    # alternativas = a ÚLTIMA sequência A, B, C, D (E) em início de linha; o artigo "A" do enunciado
    # também abre linha, então a busca é de trás para frente
    idx = {c: [i for i, s in enumerate(ls) if (m := ALT.match(s)) and m.group(1) == c] for c in "ABCDE"}
    melhor = None
    for ia in reversed(idx["A"]):
        seq, ult = [ia], ia
        for c in "BCDE"[:NALT - 1]:
            nx = [i for i in idx[c] if i > ult]
            if not nx:
                break
            ult = nx[0]; seq.append(ult)
        if len(seq) >= 4:
            melhor = seq; break
    if not melhor:
        return junta(ls), []
    enun = ls[:melhor[0]]
    alts = []
    for k, ini in enumerate(melhor):
        fim = melhor[k + 1] if k + 1 < len(melhor) else len(ls)
        bloco = ls[ini:fim]
        bloco[0] = ALT.match(bloco[0]).group(2)
        bloco = [b for b in bloco if b]
        alts.append(junta(bloco))
    return junta(enun), alts

def main():
    global NALT
    ident, arq, estilo = sys.argv[1:4]
    NALT = 4 if estilo in ("revalida", "usp") else 5
    texto = tira_numero_de_pagina(pathlib.Path(arq).read_text(encoding="utf-8", errors="replace"))
    b = blocos(texto, estilo)
    out = []
    for n in sorted(b):
        q, alts = separa(b[n], estilo)
        q = re.sub(r"^\d+\.\s*ITEM\s+\d+\s*-\s*V\.\s*\d+\s*", "", q)
        for a, z, txt in COMP:
            if a <= n <= z:
                q = junta(limpa(txt)) + " " + q
        av = []
        if any(not x.strip() for x in alts):
            av.append("alternativa vazia (figura)")
        if len(alts) not in (4, 5):
            av.append(f"{len(alts)} alternativas")
        if re.search(r"\b(figura|imagem|gráfico|tabela|eletrocardiograma a seguir|radiografia a seguir|a seguir)\b", q, re.I):
            av.append("pode depender de figura")
        if len(q) < 60:
            av.append("enunciado curto")
        out.append({"n": n, "q": q, "alts": alts, "avisos": av})
    pathlib.Path("parsed").mkdir(exist_ok=True)
    json.dump(out, open(f"parsed/{ident}.json", "w"), ensure_ascii=False, indent=1)
    falt = [i for i in range(1, max(b) + 1) if i not in b] if b else []
    print(f"{ident}: {len(out)} questões, faltando {falt[:15]}, com aviso {sum(1 for x in out if x['avisos'])}")

if __name__ == "__main__":
    main()
