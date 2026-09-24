"""Tudo que transforma um arquivo de vídeo na entrada do modelo.

Esqueleto, implementado nas Fases 1 (filtro ffmpeg usado na extração do treino) e 3.

O mesmo filtro ffmpeg (5 fps pelo tempo do vídeo, lado menor com 224 px) e o mesmo recorte central
com normalização ImageNet servem ao treino e à API (Fase 1, R7, observação 14; ADR 0002). Também
confere com ffprobe a duração, o formato e a orientação antes da análise (Fase 4).

Dependências permitidas: numpy e a biblioteca padrão (ffprobe e ffmpeg via subprocess, sem shell).
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

FPS = 5
LADO_MENOR_PX = 224
MEDIA_IMAGENET = (0.485, 0.456, 0.406)
DESVIO_IMAGENET = (0.229, 0.224, 0.225)


@dataclass(frozen=True)
class InfoVideo:
    duracao_s: float
    largura: int
    altura: int
    formato: str


def inspecionar(caminho: Path) -> InfoVideo:
    """Lê duração, dimensões (já com a rotação aplicada) e formato com ffprobe."""
    raise NotImplementedError("Fase 3")


def filtro_ffmpeg() -> str:
    """Cadeia de filtros compartilhada pelo treino e pela API."""
    raise NotImplementedError("Fase 1")


def extrair_frames(caminho: Path) -> np.ndarray:
    """Frames RGB uint8 (N x H x W x 3) a 5 fps, lado menor com 224 px."""
    raise NotImplementedError("Fase 3")


def preparar_entrada(frames: np.ndarray) -> np.ndarray:
    """Recorte central 224 x 224 e normalização ImageNet: float32 (N x 3 x 224 x 224)."""
    raise NotImplementedError("Fase 3")
