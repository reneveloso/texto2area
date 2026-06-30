"""Carrega o modelo treinado e classifica texto cru na grande area CAPES."""
from pathlib import Path

import joblib
import numpy as np

from ._preprocess import preparar

_DATA = Path(__file__).resolve().parent / "data"

# SEGURANCA: joblib.load executa codigo ao desserializar. Carregamos SOMENTE os
# artefatos versionados deste pacote.
_VEC = joblib.load(_DATA / "vetorizador.joblib")
_CLF = joblib.load(_DATA / "modelo.joblib")
_FEATS = np.array(_VEC.get_feature_names_out())
_VOCAB_NG = frozenset(f for f in _FEATS if "_" in f)


def classificar(texto, topo=5):
    """Retorna (grande_area, margens_por_classe, termos_decisivos).

    `texto`: titulo e/ou resumo CRU, em portugues.
    `margens`: lista [(classe, valor decision_function)] em ordem decrescente.
    `termos_decisivos`: termos do texto que mais empurraram a classe vencedora.
    """
    s = preparar(texto, _VOCAB_NG)
    X = _VEC.transform([s])
    area = _CLF.predict(X)[0]
    margens = sorted(
        ((c, float(m)) for c, m in zip(_CLF.classes_, _CLF.decision_function(X)[0])),
        key=lambda t: -t[1],
    )
    k = list(_CLF.classes_).index(area)
    pres = X.indices
    if len(pres):
        contrib = X.data * _CLF.coef_[k, pres]
        termos = list(_FEATS[pres[np.argsort(contrib)[::-1][:topo]]])
    else:
        termos = []
    return area, margens, termos
