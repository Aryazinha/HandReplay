# ADR 0003 — Contrato JSON versionado com Pydantic

- **Status:** aceito
- **Data:** 24/09/2026

## Contexto

"O JSON é o contrato entre back-end e front-end. Toda regra é calculada no Python, e a tela só lê e formata" (Fase 3). A Fase 4 pede o "JSON validado pelo Pydantic", e a observação 16a aceitou o contrato com Pydantic.

Desde o ADR 0005, front e API são publicados em momentos diferentes. Além disso, o JSON aparece em três lugares: na resposta da API, no "Baixar relatório" e nos exemplos pré-calculados em `app/exemplos/`.

## Decisão

- **O contrato fica em `src/handreplay/contrato.py`,** com Pydantic v2, `extra="forbid"` e modelos imutáveis.
  - `Resultado` é a resposta HTTP 200.
  - `RespostaErro` traz `{versao, erro: {codigo, mensagem}}`. Os quatro códigos do plano mapeiam para 413, 415 e 422 (`STATUS_HTTP`).
- **Invariantes conferidas na validação:**
  - 6 passos em ordem;
  - status coerente com o tempo;
  - trechos contíguos, cobrindo de 0 a `duracao_s`;
  - tempo de cada passo igual à soma dos seus trechos;
  - faixa coerente com a nota;
  - as 7 regiões presentes;
  - resumo coerente com os passos.
- **Adições aprovadas ao quadro do plano (P14):** `versao` como `{contrato, modelo, regras}`, `passos[].nome_curto`, `frase_card` como `{texto, destaque}` e `orientacao`.
- **`versao.contrato` segue o semver.**
  - O major muda quando um campo sai, muda de nome ou muda de tipo.
  - O front recusa um major diferente do seu.
  - Ordem de publicação: a API com o novo major sai primeiro, e o front sai depois.
- **O exemplo dos mockups** (nota 72) fica em `tests/dados/resultado_exemplo_72.json` e é validado em `tests/test_contrato.py`. A partir da Fase 7, `tests/test_repositorio.py` também valida `app/exemplos/*.json`.

## Consequências

- Uma mudança de formato quebra os testes antes de chegar ao front.
- O front não precisa repetir regra nenhuma.
- O JSON Schema exportado continua adiado (observação 16c). Se for necessário, ele pode ser gerado a partir dos mesmos modelos com `Resultado.model_json_schema()`.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Dicionários sem validação | O front descobriria as mudanças quebrando em produção. |
| JSON Schema escrito à mão como fonte | Duplicaria os modelos Pydantic que a API já usa. |
| Não versionar o contrato | Com front e API publicados separadamente, uma incompatibilidade passaria sem aviso. |
