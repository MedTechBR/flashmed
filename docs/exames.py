"""Tabela canônica das provas reais do FlashMed.

Cada questão de prova real carrega `fonte = {banca, ano, prova, ex, n}`:
  ex = id da prova (agrupa a prova "na íntegra" no Simulado), n = número da questão no caderno
  (quando conhecido). As questões importadas do ClínicaMed e do CirurgiaMed têm `fonte` em formatos
  antigos (sem `prova`); o monta_banco.py normaliza tudo por esta tabela, casando a CHAVE da questão
  com o índice docs/ordem.json (gerado por importa.py a partir dos cadernos extraídos).
"""
EXAMES = {
 # id: (banca, ano, prova (rótulo exibido), tipo)
 "rev2021":   ("Revalida (INEP/MEC)", 2021, "Revalida 2021", "revalida"),
 "rev2022_2": ("Revalida (INEP/MEC)", 2022, "Revalida 2022.2", "revalida"),
 "rev2023_1": ("Revalida (INEP/MEC)", 2023, "Revalida 2023.1", "revalida"),
 "rev2023_2": ("Revalida (INEP/MEC)", 2023, "Revalida 2023.2", "revalida"),
 "rev2024_1": ("Revalida (INEP/MEC)", 2024, "Revalida 2024.1", "revalida"),
 "rev2024_2": ("Revalida (INEP/MEC)", 2024, "Revalida 2024.2", "revalida"),
 "rev2025_1": ("Revalida (INEP/MEC)", 2025, "Revalida 2025.1", "revalida"),
 "rev2025_2": ("Revalida/ENAMED (INEP/MEC)", 2025, "Revalida 2025.2 (questões comuns ao ENAMED 2025)", "revalida"),
 "rev2026_1": ("Revalida (INEP/MEC)", 2026, "Revalida 2026.1", "revalida"),
 "enare24ad": ("ENARE (EBSERH/FGV)", 2024, "ENARE 2024/2025 Acesso Direto", "enare"),
 "enare24cm": ("ENARE pré-requisito (EBSERH/FGV)", 2024, "ENARE 2024/2025 pré-requisito em Clínica Médica", "prereq"),
 "enare25cm": ("ENARE pré-requisito (EBSERH/FGV)", 2025, "ENARE 2025/2026 pré-requisito em Clínica Médica", "prereq"),
 "enare24cg": ("ENARE pré-requisito (EBSERH/FGV)", 2024, "ENARE 2024/2025 pré-requisito em Cirurgia Geral", "prereq"),
 "enare25cg": ("ENARE pré-requisito (EBSERH/FGV)", 2025, "ENARE 2025/2026 pré-requisito em Cirurgia Geral", "prereq"),
 "usp26ad":   ("USP (FUVEST)", 2026, "USP 2026 Acesso Direto", "usp"),
 "usp25ad":   ("USP (FUVEST)", 2025, "USP 2025 Acesso Direto", "usp"),
 "usp25ecm":  ("USP (FUVEST)", 2025, "USP 2025 Especialidades Clínicas", "prereq"),
 "usp26ecm":  ("USP (FUVEST)", 2026, "USP 2026 Especialidades Clínicas", "prereq"),
 "usp26epd":  ("USP (FUVEST)", 2026, "USP 2026 Especialidades Pediátricas", "prereq"),
 "usp26aa":   ("USP (FUVEST)", 2026, "USP 2026 Ano Adicional em Clínica Médica", "prereq"),
 "usp25ec":   ("USP (FUVEST)", 2025, "USP 2025 Especialidades Cirúrgicas", "prereq"),
 "usp26ec":   ("USP (FUVEST)", 2026, "USP 2026 Especialidades Cirúrgicas", "prereq"),
}
# prefixo do id de origem (candidatas.json do ClínicaMed, SIMULADOS do FlashMed antigo, cand_cir.json do CirurgiaMed) → exame
ORIGEM = {
 "rev2021_pv":"rev2021", "rev2023_1_pv":"rev2023_1", "rev2023_2_pv":"rev2023_2", "rev2025_1_pv":"rev2025_1",
 "rev2025_2_pv":"rev2025_2", "rev2026_1_pv":"rev2026_1", "en24_pr_cardio":"enare24cm", "en25_pr_cardio":"enare25cm",
 "usp25_ecm":"usp25ecm", "usp26_aa":"usp26aa",
 "enare2024_ad":"enare24ad", "revalida_2022_2":"rev2022_2", "revalida_2024_1":"rev2024_1", "revalida_2024_2":"rev2024_2",
 "rm2026_ad":"usp26ad", "usp25ad":"usp25ad", "rm2026_ecm":"usp26ecm", "rm2026_epd":"usp26epd",
 "en24-cg":"enare24cg", "en25-cg":"enare25cg", "usp25-cir":"usp25ec", "usp25-cad":"usp25ec", "usp26-cir":"usp26ec", "usp26-cad":"usp26ec",
}
def fonte(ex, n=None):
    b, a, p, _ = EXAMES[ex]
    f = {"banca": b, "ano": a, "prova": p, "ex": ex}
    if n: f["n"] = int(n)
    return f
