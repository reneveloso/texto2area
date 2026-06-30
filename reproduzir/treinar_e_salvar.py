"""
Treina a versao CANONICA do classificador (corpus completo, lemmas_ext, min_df=50,
LinearSVC) e salva o artefato publicavel:

  stopwords.txt        (combina as 3 listas do projeto -> autocontido)
  vetorizador.joblib   (TF-IDF; analyzer = modelo_lib.tokenizar)
  modelo.joblib        (LinearSVC one-vs-rest, class_weight=balanced)
  classes.json         (ordem das classes)

Roda UMA vez. Determinístico (SEED=42).
Uso:  .venv/bin/python artigo/eventos/enmc_paper/modelo_publicacao/treinar_e_salvar.py
"""
from pathlib import Path
import json
import sys
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from modelo_lib import tokenizar  # noqa: E402

# localizar a raiz do repo (camada1a) subindo ate achar data/td/interim
ROOT = HERE
while not (ROOT / "data" / "td" / "interim").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
EXT = ROOT / "data" / "td" / "interim" / "corpus_consolidado_normalizado_pt_ext.parquet"
SW_SRC = ROOT / "artefatos" / "stopwords"
SEED, MIN_DF, COL = 42, 50, "lemmas_ext"

# 1) stopwords combinadas -> autocontido no pacote
sw = []
for nome in ["classicas_universais.txt", "academicas_v2.txt", "academicas_v2_ngramas.txt"]:
    p = SW_SRC / nome
    if p.exists():
        sw += [w.strip() for w in p.read_text(encoding="utf-8").splitlines()
               if w.strip() and not w.startswith("#")]
(HERE / "stopwords.txt").write_text("\n".join(sorted(set(sw))) + "\n", encoding="utf-8")
print(f"stopwords.txt: {len(set(sw)):,} termos", flush=True)

# 2) corpus COMPLETO (treina em 100% dos dados para o artefato final)
print(f"Lendo {EXT} ...", flush=True)
df = pd.read_parquet(EXT, columns=["grande_area", COL]).dropna(subset=["grande_area", COL])
df = df[df[COL].str.strip() != ""]
print(f"  {len(df):,} documentos.", flush=True)

# 3) vetorizar + treinar
vec = TfidfVectorizer(analyzer=tokenizar, min_df=MIN_DF, sublinear_tf=True)
print("Vetorizando (corpus completo, min_df=50) ...", flush=True)
X = vec.fit_transform(df[COL].values)
y = df["grande_area"].values
print(f"  features: {X.shape[1]:,}; treinando LinearSVC ...", flush=True)
clf = LinearSVC(class_weight="balanced", C=1.0, random_state=SEED)
clf.fit(X, y)

# 4) salvar
joblib.dump(vec, HERE / "vetorizador.joblib")
joblib.dump(clf, HERE / "modelo.joblib")
(HERE / "classes.json").write_text(json.dumps(list(clf.classes_), ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Salvos: vetorizador.joblib, modelo.joblib, classes.json em {HERE}", flush=True)
