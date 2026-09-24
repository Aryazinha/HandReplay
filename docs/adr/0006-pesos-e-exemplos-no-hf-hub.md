# ADR 0006 — Pesos e vídeos de exemplo em repositórios do HF Hub

- **Status:** aceito
- **Data:** 24/09/2026

## Contexto

- **Nada disso pode ir para o GitHub:** nem os pesos `.onnx`, nem os 3 vídeos de exemplo, que são do PSKUS, com licença CC BY-SA 4.0.
- **Mas os dois precisam estar disponíveis:** o `.onnx` para construir a imagem da API, e os vídeos para o front no GitHub Pages (ADR 0005).
- **Cada exemplo** precisa aparecer com a atribuição aos autores e a licença (Fase 7).

## Decisão

- **Dois repositórios públicos no HF Hub, usados só como armazenamento** (nenhum Space):
  - um repositório de modelo com o `handreplay.onnx`;
  - um repositório de dataset com os 3 vídeos e um README com a atribuição e a licença CC BY-SA 4.0.
- **Sempre pelo commit completo e com checksum:**
  - **Imagem da API** (Fase 4): o Dockerfile usa `ADD --checksum=sha256:...` com a URL `resolve/<commit>` do repositório de modelo.
  - **GitHub Pages** (Fase 5): o workflow baixa os vídeos pelo commit, confere o sha256 e os publica junto com `app/`.
- **O JSON dos exemplos** é gerado no PC com `python -m handreplay` e versionado em `app/exemplos/` (A2).
- **O model card no Hub continua adiado** (observação 17). O repositório de modelo existe só como armazenamento.

## Consequências

- GitHub e imagem da API recebem o mesmo código, e nenhum binário entra em repositório de código.
- A revisão do modelo fica rastreável: o commit está fixado no Dockerfile, e o `.onnx` traz a versão nos metadados.
- Com repositórios privados, o build passaria a precisar de `HF_TOKEN` via `docker build --secret`. A visibilidade e a licença dos pesos treinados com dados CC BY-SA são a pendência P3.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Git LFS no GitHub | Versionaria pesos e dados de terceiros no repositório do código. |
| Arquivos dentro de um Space | O Space Docker foi descartado (ADR 0005), e o Space estático é só plano B. |
| Anexos de release no GitHub | Misturaria dados de terceiros com as releases do código. |
