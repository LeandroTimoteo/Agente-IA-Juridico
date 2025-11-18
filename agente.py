def classificar_acao(texto: str) -> str:
    texto = texto.lower()
    if "relação de trabalho" in texto or "salário" in texto or "emprego" in texto:
        return "trabalhista"
    elif "contrato" in texto or "indenização" in texto or "dívida" in texto:
        return "civil"
    elif "crime" in texto or "pena" in texto or "acusado" in texto:
        return "penal"
    else:
        return "desconhecido"

