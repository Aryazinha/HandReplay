# ADR 0002 — Dois pacotes (offline × API) e o mesmo pré-processamento no treino e na API

- **Status:** aceito
- **Data:** 24/09/2026
- **Incorpora:** o antigo ADR 0007 (mesmo pré-processamento no treino e no app)

## Contexto

O plano tem duas exigências que puxam em direções opostas:

1. **Torch fora da produção.** A API roda em CPU com ONNX Runtime (Fase 2), e o pedido proíbe torch na imagem.
2. **O mesmo código dos dois lados.**
   - "Extrair frames com ffmpeg a 5 fps, pelo tempo do vídeo, com o lado menor em 224 px e a proporção mantida. O app usa o mesmo comando" (Fase 1).
   - "Na validação, no teste e no app, usar o recorte central de 224×224" (Fase 2, R7).
   - As métricas do produto aplicam as mesmas regras às anotações humanas (Fase 3).
   - A observação 14 justifica o ffmpeg justamente por tratar a rotação e o frame rate variável "com o mesmo comando no treino e no app".

## Decisão

- **Dois pacotes em `src/`:**
  - `handreplay`: a API e o núcleo compartilhado. É o que entra na imagem.
  - `handreplay_offline`: preparação no PC, treino e exportação no Kaggle, e métricas. Nunca entra na imagem.
- **Regras de importação, verificadas pelo import-linter** (`pyproject.toml`):
  1. `handreplay` nunca importa `handreplay_offline`.
  2. `handreplay` nunca importa torch, torchvision, onnx, onnxscript, pandas nem matplotlib.
  3. `sementes`, `anotacoes`, `dados` e `avaliacao` nunca importam torch, porque rodam no PC. Por isso, a semente do torch fica em `treino`.
  4. Não há dependências circulares (`acyclic_siblings`).
- **O mesmo pré-processamento, com uma única fonte, em `handreplay.video`:**
  - `filtro_ffmpeg()`: `fps=5` e escala do lado menor para 224 px. É usado para gravar os JPEG do treino e para o `rawvideo` da API.
  - `preparar_entrada()`: recorte central de 224 × 224 e normalização ImageNet, em numpy. É usado na validação e no teste do treino, na paridade da exportação e na API.
  - A ordem das classes (`contrato.CLASSES_MODELO`) é gravada nos metadados do `.onnx` e conferida pela API ao carregar o modelo.
- **Como o Kaggle recebe o código:** o notebook clona o repositório num commit fixo e o instala com `pip install -e .`, sem cópias soltas.

## Consequências

- A imagem da API instala só `requirements.txt`, e um teste falha se torch aparecer lá.
- Uma mudança no pré-processamento vale para o treino e para a API ao mesmo tempo, e exige retreinar.
- Diferenças que sobram, como a compressão JPEG no treino e a versão do ffmpeg (9.0 no PC; a da imagem ainda não foi conferida), são as pendências P5 e P7. Serão medidas comparando os frames de um mesmo vídeo nos dois caminhos.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Um pacote só, com o treino junto | A fronteira dependeria de disciplina; bastaria um import para levar torch à imagem. |
| Copiar o pré-processamento para o notebook | Duas cópias divergem sem aviso, e é exatamente isso que o plano quer evitar. |
| Pré-processar com torchvision também na API | Levaria torch para a produção. |
