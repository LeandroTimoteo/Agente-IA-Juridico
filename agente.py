def classificar_acao(texto: str) -> str:
    texto = texto.lower()

    trabalhista = ["relação de trabalho", "salário", "emprego", "demissão", "fgts"]
    civil = ["contrato", "indenização", "dívida", "aluguel", "herança"]
    penal = ["crime", "pena", "acusado", "prisão", "homicídio"]

    if any(palavra in texto for palavra in trabalhista):
        return "trabalhista"
    elif any(palavra in texto for palavra in civil):
        return "civil"
    elif any(palavra in texto for palavra in penal):
        return "penal"
    else:
        return "desconhecido"

