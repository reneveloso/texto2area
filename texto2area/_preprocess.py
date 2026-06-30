"""
Pre-processamento ponta-a-ponta: texto cru (PT) -> string no formato do corpus
(lemas de conteudo + n-gramas unidos por '_'). Reproduz fielmente o pipeline de
treino (Camada 1a, etapas 2-3):

  - normalizacao: NFC + remocao de controles + colapso de espacos;
  - lematizacao: spaCy pt_core_news_lg, mantendo apenas POS de conteudo
    (NOUN, PROPN, ADJ, VERB), lemma minusculo, len>=2, com letra;
  - n-gramas: bi/trigramas adjacentes unidos por '_', mantidos os que existem
    no vocabulario do modelo.

Idioma: PORTUGUES. Para textos em outro idioma, traduza antes (ver README).
"""
import re
import unicodedata

import spacy

POS_MANTER = {"NOUN", "PROPN", "ADJ", "VERB"}
SPACY_MODELO = "pt_core_news_lg"
_RX_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_RX_ESPACOS = re.compile(r"\s+")
_NLP = None


def _nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load(SPACY_MODELO, exclude=["parser", "ner", "senter"])
    return _NLP


def normalizar(texto):
    t = unicodedata.normalize("NFC", texto or "")
    t = _RX_CONTROLE.sub(" ", t)
    t = _RX_ESPACOS.sub(" ", t)
    return t.strip()


def lematizar(texto):
    """Lista de lemas de conteudo (mesma regra do treino)."""
    doc = _nlp()(normalizar(texto))
    out = []
    for t in doc:
        if t.pos_ not in POS_MANTER:
            continue
        l = t.lemma_.lower().strip()
        if len(l) >= 2 and any(c.isalpha() for c in l):
            out.append(l)
    return out


def preparar(texto, vocab_ngramas=frozenset()):
    """Texto cru -> string 'lemmas_ext' (lemas + n-gramas conhecidos)."""
    lemas = lematizar(texto)
    extra = []
    for n in (2, 3):
        for i in range(len(lemas) - n + 1):
            j = "_".join(lemas[i:i + n])
            if j in vocab_ngramas:
                extra.append(j)
    return " ".join(lemas + extra)
