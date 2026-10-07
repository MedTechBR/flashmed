import re
CONJ=re.compile(r"^(e|ou|mas|nem|porque|pois|como|sem|com|em|de|do|da|dos|das|no|na|nos|nas|num|numa|para|por|até|desde|se|quando|onde|entre|sob|sobre|contra|ainda|inclusive|sobretudo|principalmente|exceto|salvo|ou seja|isto é|isso|o que|a que)\b")
def _par(m):
    a,x,b=m.group(1),m.group(2).strip(),m.group(3)
    if "," in x: return f"{a}({x}){b}"
    return f"{a}, {x}{b}"
def _solo(m):
    antes,resto=m.group(1),m.group(2)
    # resto = até o fim da frase (sem ponto final)
    w=resto.split()
    if resto[:1].islower():
        if CONJ.match(resto) or len(w)<6: return antes+", "+resto
        return antes+". "+resto[0].upper()+resto[1:]
    if len(w)<=5: return antes+": "+resto
    return antes+". "+resto
def limpa(t):
    if "—" not in t: return t
    # 1) parentético fechado por pontuação:  " — X —,"  → ", X,"  ou "(X),"
    t=re.sub(r"(\S)\s—\s([^—<>]{1,180}?)\s—(?=[,.;:)])",lambda m:_par((m.group(1),m.group(2),"")) if False else (f"{m.group(1)} ({m.group(2).strip()})" if "," in m.group(2) else f"{m.group(1)}, {m.group(2).strip()}"),t)
    # 2) parentético seguido de espaço:  " — X — "  → ", X, "
    t=re.sub(r"(\S)\s—\s([^—<>]{1,180}?)\s—\s",lambda m:(f"{m.group(1)} ({m.group(2).strip()}) " if "," in m.group(2) else f"{m.group(1)}, {m.group(2).strip()}, "),t)
    # 3) travessão solto: decide pelo que vem depois, até o fim da frase
    t=re.sub(r"(\S)\s—\s(?=\S)([^.!?;<>—]{1,240}?)(?=[.!?;<>—]|$)",_solo,t)
    t=re.sub(r"^\s*—\s+(?=\S)",", ",t)
    # 4) sobras: "—," / "—." / " —" no fim de trecho
    t=re.sub(r"\s?—(?=[,.;:)])","",t)
    t=re.sub(r"\s—\s*$",",",t); t=re.sub(r"\s—\s",", ",t)
    # 5) artefatos
    t=re.sub(r",\s*,",",",t); t=re.sub(r":\s*,",":",t); t=re.sub(r",\s*\.",".",t); t=re.sub(r"\(\s*,",'(',t)
    return t
def limpa_html(s):
    partes=re.split(r"(<script.*?</script>|<style.*?</style>|<pre.*?</pre>|<[^>]+>)",s,flags=re.S)
    return "".join(p if (p.startswith("<")) else limpa(p) for p in partes)
