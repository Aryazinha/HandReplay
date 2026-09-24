"""API HTTP: ``POST /analisar``, ``GET /saude`` e CORS restrito à origem do front.

Esqueleto, implementado na Fase 4.

- ``POST /analisar`` (campo multipart ``video``): copia o upload em blocos para um arquivo
  temporário de nome aleatório, contando os bytes (``arquivo_grande``), chama
  ``pipeline.analisar`` e apaga o arquivo num ``finally``. Declarada com ``def`` para rodar no
  threadpool. Nada é guardado entre requisições.
- ``GET /saude``: ``{"status": "ok", "versao": {...}}``, sem tocar no modelo nem em arquivos.
  O front só a chama quando a pessoa abre o painel "Enviar vídeo" (A1).
- CORS via ``CORSMiddleware`` com ``Config.origens``; a API não serve o front (ADR 0005).
- O modelo é carregado uma vez no ``lifespan``.

Dependências permitidas: fastapi, config, contrato, modelo e pipeline.
"""

from fastapi import FastAPI

from handreplay.config import Config


def criar_app(config: Config | None = None) -> FastAPI:
    """Cria a aplicação; sem ``config``, lê as variáveis de ambiente."""
    raise NotImplementedError("Fase 4")
