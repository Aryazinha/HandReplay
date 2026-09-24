"""Preparação dos dados da Fase 1, no PC local.

Esqueleto, implementado na Fase 1.

- Extrai os frames com o mesmo filtro ffmpeg da API (``handreplay.video.filtro_ffmpeg``).
- Divide como os autores: o local de teste do PSKUS ("Reanimācija", grafia a confirmar na Fase 0)
  é o teste; os demais locais conhecidos se dividem por vídeo em treino (85%) e validação (15%),
  com ``sementes.gerador``; vídeos de local desconhecido ficam de fora; o METC inteiro é teste.
- Monta o índice (frame, rótulo, vídeo, local, divisão) e o gráfico da distribuição das classes.

Os dados ficam em ``Config.dir_dados`` (HANDREPLAY_DADOS), fora do git.

Dependências permitidas: pandas, matplotlib, ``anotacoes``, ``sementes`` e ``handreplay.video``.
Nunca torch.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from handreplay_offline.sementes import SEMENTE

if TYPE_CHECKING:
    import pandas as pd

PROPORCAO_VALIDACAO = 0.15


def extrair_frames_jpeg(video: Path, destino: Path) -> int:
    """Grava os frames de um vídeo como JPEG e devolve quantos foram gravados."""
    raise NotImplementedError("Fase 1")


def dividir_por_local(videos: "pd.DataFrame", semente: int = SEMENTE) -> "pd.DataFrame":
    """Acrescenta a coluna ``divisao`` (treino, validacao, teste, teste_metc ou fora)."""
    raise NotImplementedError("Fase 1")


def montar_indice(dir_dados: Path) -> "pd.DataFrame":
    """Índice com uma linha por frame: frame, rótulo, vídeo, local e divisão."""
    raise NotImplementedError("Fase 1")


def grafico_classes(indice: "pd.DataFrame", destino: Path) -> None:
    """Salva o gráfico com o número de frames por classe e divisão."""
    raise NotImplementedError("Fase 1")
