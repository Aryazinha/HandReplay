# HandReplay

App web educativo que recebe um vídeo de lavagem de mãos e devolve:

- um replay comentado;
- um mapa de cobertura das mãos;
- uma nota;
- um card para compartilhar.

Com isso, a pessoa vê o que fez bem, o que faltou e como fazer o passo que faltou, segundo os 6 movimentos de fricção da OMS.

> **Ferramenta educativa.** O HandReplay não substitui treinamento nem avaliação de controle de infecção. A análise é estimada por IA.

**Situação:** estrutura base pronta, prestes a começar a Fase 0. Modelo, pipeline e telas ainda não foram implementados.

## Arquitetura em uma página

| Parte | Onde roda | Código |
|---|---|---|
| Preparação dos dados e métricas do produto | PC local | `src/handreplay_offline/` |
| Treino da MobileNetV2, calibração e exportação ONNX | Kaggle (GPU) | `src/handreplay_offline/` |
| API: `POST /analisar` e `GET /saude` | Container portátil em CPU (recomendado: Azure Container Apps pelo Azure for Students) | `src/handreplay/` |
| Front: tela Analisar e card | GitHub Pages; funciona sem a API, com 3 exemplos | `app/` |

- O `handreplay` nunca importa torch, e o `handreplay_offline` nunca entra na imagem da API. O import-linter confere essas regras.
- O JSON de resultado é um contrato versionado (`src/handreplay/contrato.py`). O front só lê e formata.
- Nada é guardado no servidor: o vídeo vai para um arquivo temporário, apagado ao fim da análise, e o card é gerado no navegador.
- O projeto tem custo zero: só serviços gratuitos ou benefícios de estudante, sem cartão de crédito.

Detalhes e justificativas:

- [docs/architecture/diagnostico-e-proposta.md](docs/architecture/diagnostico-e-proposta.md)
- os ADRs em [docs/adr/](docs/adr/README.md)
- as telas de referência em [docs/referencia/](docs/referencia/)

## Estrutura

```
src/handreplay/          API + núcleo compartilhado (contrato, regras, vídeo, modelo)
src/handreplay_offline/  preparação dos dados, treino, exportação e métricas
app/                     front-end estático (Fases 5 a 7)
notebooks/               notebooks finos, um por fase (sem saídas no git)
data/                    dados locais, fora do git (veja data/README.md)
tests/                   pytest
docs/                    diagnóstico, ADRs, referência visual e roteiro de gravação
```

## Preparar o ambiente (PC)

Pré-requisitos: Python 3.12 e ffmpeg/ffprobe no PATH.

PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pip install -e .
Copy-Item .env.example .env   # e ajuste HANDREPLAY_DADOS para fora do OneDrive
```

Para as Fases 0, 1 e 3, instale também as dependências offline:

```powershell
python -m pip install -r requirements-treino.txt
```

| Arquivo | Para quê |
|---|---|
| `requirements.txt` | Produção (imagem da API). Versões exatas, sem torch. |
| `requirements-treino.txt` | PC e Kaggle. Faixas mínimas, para não reinstalar o torch do Kaggle. |
| `requirements-dev.txt` | Produção + testes, lint e pre-commit. |

## Qualidade

Rode os quatro comandos antes de cada commit. Todos devem passar.

```powershell
pytest
ruff check .
ruff format --check .
lint-imports
```

- **pytest.**
  - `tests/test_contrato.py` valida o exemplo dos mockups (nota 72) e recusa resultados incoerentes.
  - `tests/test_regras.py` traz os cinco casos fixos da Fase 3 como *xfail estrito*. Quando as regras forem implementadas, eles passam a passar, o pytest acusa, e o marcador tem que ser removido.
  - `tests/test_repositorio.py` garante que:
    - não há torch em `requirements.txt`;
    - as versões de produção são exatas;
    - todos os módulos de `handreplay` importam sem torch;
    - os notebooks estão sem saídas;
    - os exemplos do front seguem o contrato.
- **ruff.** Lint (regras E, F, W, I, B, UP, SIM e RUF) e formatação, com alvo Python 3.11 e linhas de 100 caracteres.
- **import-linter.** Os cinco contratos de `pyproject.toml`:
  1. a API não importa o pacote offline;
  2. a API não importa dependências de treino;
  3. a preparação de dados roda sem torch;
  4. as camadas do pacote `handreplay`;
  5. não há dependências circulares.
- **pre-commit** (`.pre-commit-config.yaml`): `ruff-check`, `ruff-format` e `nbstripout`. O `nbstripout` apaga as saídas dos notebooks, que podem conter frames de dados de terceiros. Ative com `pre-commit install` depois do `git init`. O git só será iniciado com a pasta fora do OneDrive.
- **Reprodutibilidade.**
  - Semente única em `handreplay_offline.sementes.SEMENTE`.
  - O treino segue a nota de reprodutibilidade do PyTorch.
  - Cada notebook grava o `pip freeze`, a semente e a versão do ffmpeg na saída.
- **Sem CI de testes** por enquanto (observação 16c do plano). O único workflow previsto publica o GitHub Pages (Fase 5).

## Como começar a Fase 0

1. Prepare o ambiente acima, com `HANDREPLAY_DADOS` numa pasta fora do OneDrive.
2. Baixe o `DataSet4.zip` do PSKUS (112 MB) e o METC (2,1 GB) do Zenodo para `HANDREPLAY_DADOS/brutos/` (veja `data/README.md`).
3. Leia o artigo do dataset (Lulla et al., 2021), o estudo de generalização (Elsts et al., 2022) e o README de [edi-riga/handwash](https://github.com/edi-riga/handwash).
4. Crie `notebooks/00_explorar_anotacoes.ipynb` e abra alguns arquivos de anotação (CSV e JSON).
   - PSKUS: códigos de 0 a 7, e o 7 vira "outro".
   - METC: códigos de 0 a 6, um anotador por vídeo, cerca de 16 fps.
   - Confirme também a grafia exata do local de teste do PSKUS.
5. Preencha [docs/roteiro-gravacao.md](docs/roteiro-gravacao.md) e marque as duas sessões de gravação.

**A Fase 0 está pronta quando** você consegue abrir um vídeo e mostrar o rótulo de cada frame lado a lado, e o roteiro de gravação está escrito.

## Dados, licenças e créditos

- **PSKUS**, Hospital Pauls Stradins (<https://zenodo.org/records/4537209>): CC BY-SA 4.0. Os vídeos de exemplo do app vêm do conjunto de teste do PSKUS e são exibidos com atribuição e licença.
- **METC** (<https://zenodo.org/records/5808789>): CC BY 4.0.
- **Lulla et al., 2021.** Hand-washing video dataset annotated according to the World Health Organization's hand-washing guidelines. *Data*, 6(4), 38. <https://doi.org/10.3390/data6040038>
- **Elsts et al., 2022.** Estudo de generalização (IPTA). <https://ieeexplore.ieee.org/document/9784153/>
- **OMS, 2009.** *WHO guidelines on hand hygiene in health care*. <https://www.who.int/publications/i/item/9789241597906>

Nenhum vídeo, frame, peso ou dado de terceiros é versionado neste repositório. Os vídeos gravados com celular para o teste ficam fora dele, e só as métricas são publicadas.

## Licença

O código é distribuído sob a licença [MIT](LICENSE). Os datasets seguem as licenças próprias listadas acima.
