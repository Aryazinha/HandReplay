# app/

Front-end estático da tela Analisar e do card, feito com HTML, CSS e JavaScript em módulos ES nativos, sem framework e sem build. É publicado no GitHub Pages (ADR 0005) e **funciona sem a API**.

## Regra principal

**O front não calcula nenhuma regra.** Nota, faixa, frases, status dos passos, trechos e mapa vêm prontos no JSON do contrato v1 (`src/handreplay/contrato.py`). O front só lê e formata. Ele confere o major de `versao.contrato` e recusa um JSON de outro major.

## Os dois modos

| Modo | Quando | O que funciona |
|---|---|---|
| Completo | `js/config.js` tem a URL da API, e `GET /saude` responde depois que a pessoa abre o painel "Enviar vídeo" | Envio de vídeo, análise, replay, card e relatório |
| Só exemplos | A URL está vazia, ou a API não responde a tempo | Os 3 exemplos com replay, HUD, mapa, passos, card e "Baixar relatório" |

A página abre com o primeiro exemplo e **não chama a API**. `GET /saude` só é chamado quando a pessoa abre o painel "Enviar vídeo". Assim, quem só vê os exemplos não acorda o container nem gasta a cota do provedor.

## Arquivos previstos

| Arquivo | Fase | Papel |
|---|---|---|
| `index.html` | 5 | Tela Analisar, painel "Enviar vídeo" e bloco "Como funciona". As abas "Por dentro da IA" e "Dados reais" ficam desabilitadas, com o rótulo "em breve". |
| `css/estilo.css` | 5 | Cores e fontes da interface de referência (`docs/referencia/`); coluna única abaixo de 900 px |
| `js/config.js` | 5 | URL da API; vazia liga o modo só exemplos |
| `js/principal.js` | 5 | Estados da tela, exemplos, `GET /saude` ao abrir o painel e envio por `XMLHttpRequest` (progresso do upload) |
| `js/resultado.js` | 5 | Nota, passos, mapa e linha do tempo |
| `js/replay.js` | 5 | HUD sincronizado pelo `timeupdate`, velocidades e "Sobreposição" |
| `js/maos.js` | 5 | Desenho das mãos compartilhado pela tela (SVG) e pelo card (`Path2D`) |
| `js/card.js` | 6 | Canvas de 1080 x 1350 e download em PNG |
| `exemplos/*.json` | 7 | Resultado dos 3 exemplos, gerado com `python -m handreplay` e validado pelos testes |

Os vídeos dos exemplos (PSKUS, CC BY-SA 4.0) não entram no git. O workflow do Pages os baixa do HF Hub no deploy, e cada vídeo é exibido com a atribuição e a licença.
