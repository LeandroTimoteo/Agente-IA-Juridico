import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agente import classificar_acao

def test_classificacao_trabalhista():
    assert classificar_acao("O funcionário busca reparação por salário não pago.") == "trabalhista"

def test_classificacao_civil():
    assert classificar_acao("A ação trata de quebra de contrato e pedido de indenização.") == "civil"

def test_classificacao_penal():
    assert classificar_acao("O réu foi acusado de crime contra a vida.") == "penal"

def test_classificacao_desconhecida():
    assert classificar_acao("Pedido genérico sem contexto jurídico claro.") == "desconhecido"



