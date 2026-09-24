"""Métricas do modelo (Fase 2) e do produto (Fase 3).

Esqueleto, implementado nas Fases 2 e 3.

- Modelo: F1 macro (métrica principal), F1 por classe, matriz de confusão, acurácia e ECE antes e
  depois da calibração, no teste do PSKUS e no METC.
- Produto: acerto do status de cada passo, precisão e revocação de "não detectado", erro médio
  absoluto da nota e fração do tempo marcada como incerta. A comparação é entre o app
  (``handreplay.pipeline``) e as anotações humanas passadas pelas mesmas regras
  (``handreplay.regras``), nos três conjuntos de teste.

Dependências permitidas: numpy, pandas, scikit-learn, ``anotacoes``, ``handreplay.pipeline`` e
``handreplay.regras``. Nunca torch.
"""

import numpy as np


def erro_calibracao_esperado(
    rotulos: np.ndarray, probabilidades: np.ndarray, n_faixas: int = 15
) -> float:
    """ECE: média ponderada de |acurácia - confiança| por faixa de confiança."""
    raise NotImplementedError("Fase 2")


def metricas_modelo(rotulos: np.ndarray, probabilidades: np.ndarray) -> dict:
    """F1 macro, F1 por classe, matriz de confusão, acurácia e ECE."""
    raise NotImplementedError("Fase 2")


def metricas_produto(conjunto: str) -> dict:
    """Métricas do produto em um conjunto de teste (pskus_teste, metc ou celular)."""
    raise NotImplementedError("Fase 3")
