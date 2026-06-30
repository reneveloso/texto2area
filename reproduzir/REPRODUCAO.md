# Reprodução

Os artefatos em `texto2area/data/` (`modelo.joblib`, `vetorizador.joblib`,
`classes.json`) foram gerados no repositório de origem do projeto (Tarrafa /
Camada 1a), que tem acesso ao corpus (Catálogo Sucupira — teses e dissertações
brasileiras, 2013–2024).

**O corpus não é redistribuído aqui.** Estes scripts documentam o processo, por
transparência:

- `treinar_e_salvar.py` — treina `LinearSVC` sobre TF-IDF (lemas + n-gramas,
  `min_df=50`) no corpus completo e salva `modelo.joblib` + `vetorizador.joblib`.
  Determinístico (`SEED=42`).
- `modelo_lib.py` — tokenizador usado no treino (split + stopwords).
- `_construir_artefatos.py` — converte o vetorizador treinado para o formato do
  pacote (troca o *analyzer* por `split`, tornando o `.joblib` autocontido) e
  copia os artefatos para `texto2area/data/`. Inclui verificação de que a troca
  de *analyzer* não altera o `transform`.

Para reexecutar é necessário o repositório de origem com o corpus. O desempenho
relatado (F1-macro 0,79 *in-distribution*; 0,73 *out-of-time*) vem dos protocolos
de avaliação descritos no `README.md`.
