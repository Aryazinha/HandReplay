"""Sessão do ONNX Runtime em CPU e metadados do modelo exportado.

Esqueleto, implementado na Fase 3.

O .onnx já traz a temperatura embutida (saída = probabilidades calibradas) e, nos metadados,
a versão e a ordem das classes gravadas na exportação. O modelo é carregado uma vez por processo
(lifespan da API ou início da linha de comando) e passado como parâmetro para ``analisar``.

Dependências permitidas: numpy e onnxruntime.
"""

from pathlib import Path

import numpy as np


class Modelo:
    """Classificador de frames: 7 probabilidades por frame, na ordem de ``CLASSES_MODELO``."""

    versao: str

    def prever(self, entrada: np.ndarray) -> np.ndarray:
        """Probabilidades float32 (N x 7) para a entrada de ``video.preparar_entrada``."""
        raise NotImplementedError("Fase 3")


def carregar(caminho: Path, threads: int) -> Modelo:
    """Abre o .onnx com o CPUExecutionProvider e confere a ordem das classes nos metadados."""
    raise NotImplementedError("Fase 3")
