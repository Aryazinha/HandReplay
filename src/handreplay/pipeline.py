"""Orquestração da análise: ``analisar(video, modelo) -> dict``.

Esqueleto, implementado na Fase 3.

Fluxo: ffprobe (limites de formato e duração) -> frames a 5 fps -> modelo ONNX calibrado ->
regras -> ``Resultado`` validado pelo contrato -> dict pronto para JSON. Falhas previstas saem como
``contrato.ErroAnalise``. Meta do plano: um vídeo de 60 s em até 30 s, em CPU.

Dependências permitidas: config, contrato, modelo, regras e video.
"""

from pathlib import Path

from handreplay.config import Config
from handreplay.modelo import Modelo


def analisar(caminho_video: Path, modelo: Modelo, config: Config) -> dict:
    """Analisa um vídeo e devolve o JSON de resultado (contrato v1) como dict."""
    raise NotImplementedError("Fase 3")
