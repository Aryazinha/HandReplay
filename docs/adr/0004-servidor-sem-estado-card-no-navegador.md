# ADR 0004 — API sem estado e card gerado no navegador

- **Status:** aceito
- **Data:** 24/09/2026

## Contexto

- **Privacidade de quem envia vídeos** (tabela de riscos do plano): "Vídeo apagado ao fim da análise, nenhuma rota que guarde resultados e card gerado no navegador".
- **Decisão 6 do plano:** "Card no navegador, sem Pillow nem GET /card/{id}", porque isso "tira o único ponto em que o servidor guardaria resultados".
- **Pedido inicial:** falava em `GET /card/{id}`. Em 23/09/2026 você escolheu seguir o plano.

## Decisão

- **A API não guarda nada entre requisições.**
- **O vídeo enviado:**
  - é copiado para um arquivo temporário de nome aleatório;
  - é analisado;
  - é apagado num `finally`, com ou sem erro;
  - nunca aparece nos logs, nem pelo nome, nem pelo conteúdo, nem pelos frames.
- **Rotas:** `POST /analisar` e `GET /saude`. Esta última foi aprovada como exceção (A1) e só devolve o status e a versão.
- **O card de 1080 × 1350 é desenhado num canvas no navegador** (`app/js/card.js`), a partir do JSON, com o mesmo desenho das mãos da tela (`app/js/maos.js`). O download sai em PNG.

## Consequências

- Não há Pillow, cache, banco nem limpeza periódica.
- A política de privacidade é simples de explicar na tela de envio.
- O card depende das fontes carregadas no navegador, por isso `card.js` espera `document.fonts.load`.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| `GET /card/{id}` com Pillow | Exigiria guardar cada resultado por id, contrariando o plano, e custaria cerca de 2 h a mais. |
| HTML convertido em imagem no servidor | Mesma necessidade de guardar estado, e um navegador headless na imagem. |
