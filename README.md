# texto2area

[![PyPI](https://img.shields.io/pypi/v/texto2area.svg)](https://pypi.org/project/texto2area/)
[![Python](https://img.shields.io/pypi/pyversions/texto2area.svg)](https://pypi.org/project/texto2area/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21082954.svg)](https://doi.org/10.5281/zenodo.21082954)

Biblioteca Python que classifica o **título e/ou resumo** de uma tese/dissertação
brasileira em uma das **9 grandes áreas de avaliação CAPES**, a partir do texto —
**ponta a ponta**: recebe texto cru em português e faz normalização, lematização,
n-gramas e classificação.

```python
from texto2area import classificar

area, margens, termos = classificar(
    "A atuação do enfermeiro no cuidado ao paciente idoso em saúde coletiva."
)
# area    -> 'CIÊNCIAS DA SAÚDE'
# margens -> [('CIÊNCIAS DA SAÚDE', 1.28), ('CIÊNCIAS BIOLÓGICAS', -1.0), ...]
# termos  -> ['saúde_coletivo', 'enfermeiro', 'paciente', 'cuidado']
```

## Instalação
```bash
pip install texto2area
python -m spacy download pt_core_news_lg     # modelo de lematização (~568 MB), obrigatório
```
Versão de desenvolvimento (GitHub): `pip install git+https://github.com/reneveloso/texto2area`
Ou, a partir de um clone: `pip install .`

## Uso pretendido e domínio de validade
- **Idioma:** português. Para textos em outro idioma, **traduza antes** (a tradução
  não é embutida — exigiria um modelo pesado).
- **Domínio:** teses e dissertações (título/resumo), 2013–2024 (Catálogo Sucupira).
  Fora disso (outros gêneros, outras taxonomias) o desempenho não é garantido.
- **Saída:** grande área + margens (`decision_function`) por classe + termos do texto
  que mais pesaram na decisão (interpretabilidade do modelo linear).

## Como funciona (fiel ao pipeline de treino)
1. Normalização (NFC, limpeza, colapso de espaços).
2. Lematização com spaCy `pt_core_news_lg`, mantendo POS de conteúdo
   (`NOUN, PROPN, ADJ, VERB`), lema minúsculo, `len>=2`.
3. Injeção de n-gramas: bi/trigramas adjacentes unidos por `_`, mantidos os que
   existem no vocabulário do modelo (85% das 359.402 features são n-gramas).
4. TF-IDF (`sublinear_tf`, `min_df=50`) + `LinearSVC` (one-vs-rest, `class_weight='balanced'`).

## Desempenho (avaliação em conjuntos retidos)
| Protocolo | Acurácia | F1-macro | Baseline (maj.) |
|---|---|---|---|
| In-distribution (split 80/20) | 0,792 | **0,791** | 0,165 |
| Out-of-time (treino ≤2023, teste 2024) | 0,729 | **0,732** | 0,170 |

F1 por área varia de Linguística/Letras/Artes 0,879 e Saúde 0,860 a
**Multidisciplinar 0,549** (classe difusa, sem vocabulário próprio). O artefato é
treinado em 100% dos dados (1.017.727 documentos); as métricas vêm dos protocolos
de avaliação.

## Limitações
- Rótulo administrativo como verdade-base (parte dos "erros" é interdisciplinaridade real).
- Multidisciplinar pouco separável (F1 0,549).
- Não distingue as ~49 áreas de avaliação finas (apenas as 9 grandes áreas).
- Português apenas (sem tradução embutida).

## Segurança
O modelo é carregado via `joblib`, que **executa código ao desserializar**. Use apenas
os artefatos versionados neste repositório ou de fonte confiável.

## Reprodução
Ver [`reproduzir/REPRODUCAO.md`](reproduzir/REPRODUCAO.md). O treino é determinístico
(`SEED=42`); o corpus (Sucupira) não é redistribuído.

## Como citar
Ver [`CITATION.cff`](CITATION.cff). DOI do Zenodo a ser adicionado.

## Licença
[MIT](LICENSE) © 2026 Renê R. Veloso.
