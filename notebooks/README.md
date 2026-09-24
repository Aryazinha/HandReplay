# notebooks/

Os notebooks são finos: a lógica fica nos pacotes `handreplay` e `handreplay_offline`, onde pode ser testada. Cada notebook é criado quando a sua fase começa.

| Notebook | Fase | Onde roda | Entrada | Saída |
|---|---|---|---|---|
| `00_explorar_anotacoes.ipynb` | 0 | PC | `DataSet4.zip` do PSKUS e o METC | Um vídeo com o rótulo de cada frame lado a lado; notas sobre o formato das anotações |
| `01_preparar_dados.ipynb` | 1 | PC | Os 11 arquivos do PSKUS e o METC | Frames, `indice.csv`, gráfico das classes e o upload para um Kaggle Dataset privado |
| `02_treinar.ipynb` | 2 | Kaggle (GPU) | Kaggle Dataset com os frames | `handreplay.onnx` calibrado, métricas do modelo e `pip freeze` |
| `03_metricas_produto.ipynb` | 3 | PC | `.onnx`, teste do PSKUS, METC e vídeos de celular | Tabela de métricas do produto |

## Regras

- **Nenhuma saída no git.** As saídas podem conter frames de dados de terceiros ou de pessoas gravadas. O hook `nbstripout` do pre-commit apaga as saídas antes de cada commit, e `tests/test_repositorio.py` falha se alguma sobrar.
- **Semente fixa:** use `handreplay_offline.sementes.fixar_sementes()` e, no treino, `handreplay_offline.treino.fixar_sementes_torch()`.
- **No Kaggle,** clone o repositório num commit fixo e instale com `pip install -e .` e `pip install -r requirements-treino.txt`. O pip mantém o torch que já vem na imagem.
