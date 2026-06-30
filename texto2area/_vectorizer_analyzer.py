"""Analyzer do vetorizador TF-IDF.

A entrada de `transform` ja vem como string de tokens separados por espaco
(lemas + n-gramas unidos por '_'), produzida por `_preprocess.preparar`.
Por isso o analyzer e' apenas `split`. Stopwords nao estao no vocabulario do
modelo, entao tokens irrelevantes sao naturalmente ignorados pelo vetorizador.

Esta funcao precisa estar importavel ao CARREGAR o vetorizador (joblib guarda
a referencia). Mantida em modulo proprio e estavel.
"""


def split_tokens(texto):
    return texto.split()
