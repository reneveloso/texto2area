"""
Smoke test: a biblioteca carrega e classifica corretamente casos obvios.

Requer:  pip install -e .  &&  python -m spacy download pt_core_news_lg
Rodar:   pytest
"""
import texto2area as t


def test_saude():
    area, margens, termos = t.classificar(
        "A atuacao do enfermeiro no cuidado ao paciente em saude coletiva.")
    assert area == "CIENCIAS DA SAUDE" or area == "CIÊNCIAS DA SAÚDE"


def test_engenharias():
    area, _, _ = t.classificar(
        "Metodo de elementos finitos para simular trincas em concreto armado.")
    assert "ENGENHARIA" in area.upper()


def test_retorno_ordenado():
    area, margens, termos = t.classificar("Estudo sobre a poesia modernista brasileira.")
    assert isinstance(area, str)
    assert isinstance(termos, list)
    # margens vem ordenada (decrescente) e a vencedora e' a primeira
    assert margens[0][0] == area
    assert margens[0][1] >= margens[1][1]
