"""
Tokenizador do classificador de grande area CAPES.

IMPORTANTE: este modulo precisa estar importavel ao CARREGAR os .joblib
(o vetorizador guarda uma referencia a `tokenizar`). Mantenha-o junto do
modelo e do arquivo `stopwords.txt`.

A entrada esperada e' texto JA PRE-PROCESSADO no formato do corpus
(lemas + n-gramas separados por espaco, minusculas). Ver MODELO.md.
"""
from pathlib import Path

_SW = None


def carregar_stopwords():
    global _SW
    if _SW is None:
        p = Path(__file__).resolve().parent / "stopwords.txt"
        _SW = {w.strip().lower() for w in p.read_text(encoding="utf-8").splitlines()
               if w.strip() and not w.startswith("#")}
    return _SW


def tokenizar(texto):
    """Split por espaco + remocao de stopwords. Reproduz o analyzer do treino."""
    sw = carregar_stopwords()
    return [t for t in texto.split() if t not in sw]
