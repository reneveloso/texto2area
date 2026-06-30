"""texto2area — classifica titulo/resumo de teses e dissertacoes brasileiras
na grande area de avaliacao CAPES, a partir do texto (portugues).

    from texto2area import classificar
    area, margens, termos = classificar("Enfermagem no cuidado ao paciente...")

Importacao preguicosa: o modelo so e' carregado no primeiro uso de `classificar`
(permite importar submodulos auxiliares sem exigir os artefatos).
"""
__version__ = "0.1.0"
__all__ = ["classificar", "preparar", "lematizar", "normalizar"]


def __getattr__(name):
    if name == "classificar":
        from ._classify import classificar
        return classificar
    if name in ("preparar", "lematizar", "normalizar"):
        from . import _preprocess
        return getattr(_preprocess, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
