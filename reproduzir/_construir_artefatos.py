"""
Constroi os artefatos do pacote a partir do modelo treinado em
`../modelo_publicacao/` (gerado por treinar_e_salvar.py):

  - troca o analyzer do vetorizador (modelo_lib.tokenizar -> texto2area split),
    tornando o .joblib autocontido no pacote;
  - copia modelo.joblib e classes.json para texto2area/data/.

Verifica que a troca de analyzer NAO altera o transform (stopwords nao estao no
vocabulario, logo split == split+stopwords para os termos do vocab).

Uso (no repo):  .venv/bin/python artigo/eventos/texto2area/_construir_artefatos.py
"""
import shutil
import sys
from pathlib import Path

import joblib
import numpy as np

HERE = Path(__file__).resolve().parent
MP = HERE.parent / "enmc_paper" / "modelo_publicacao"   # modelo treinado (origem)
sys.path.insert(0, str(HERE))                   # para importar texto2area._vectorizer_analyzer
sys.path.insert(0, str(MP))                     # para resolver modelo_lib do vec antigo

import texto2area._vectorizer_analyzer as va    # noqa: E402

DATA = HERE / "texto2area" / "data"
DATA.mkdir(parents=True, exist_ok=True)

print("Carregando vetorizador treinado ...", flush=True)
vec = joblib.load(MP / "vetorizador.joblib")

# verificacao: transform identico antes/depois da troca de analyzer
amostra = "elemento finito simulacao trinca concreto_armado estrutura conclusao trabalho"
X_old = vec.transform([amostra])
vec.analyzer = va.split_tokens
X_new = vec.transform([amostra])
assert (X_old != X_new).nnz == 0, "troca de analyzer alterou o transform!"
print("  OK: troca de analyzer preserva o transform.", flush=True)

joblib.dump(vec, DATA / "vetorizador.joblib")
shutil.copy(MP / "modelo.joblib", DATA / "modelo.joblib")
shutil.copy(MP / "classes.json", DATA / "classes.json")
print(f"Artefatos em {DATA}: vetorizador.joblib, modelo.joblib, classes.json", flush=True)
