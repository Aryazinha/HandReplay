"""Leitura das anotações do PSKUS e do METC e montagem do rótulo de cada frame.

Esqueleto, implementado nas Fases 0 e 1.

- PSKUS: códigos de 0 a 7 e vários anotadores. Votação por maioria (mais da metade), com descarte
  dos frames sem consenso. O código 7 (fechar a torneira com papel) vira "outro".
- METC: códigos de 0 a 6, um anotador por vídeo, cerca de 16 fps; vale a anotação única.
- Os frames a menos de 0,5 s de cada troca de movimento são ignorados (atraso dos anotadores).

O formato exato dos arquivos (CSV e JSON) é confirmado na Fase 0, seguindo o repositório
edi-riga/handwash. As mesmas funções servem às métricas do produto (Fase 3).

Dependências permitidas: pandas e ``handreplay.contrato``. Nunca torch.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

MARGEM_TROCA_S = 0.5


def ler_pskus(pasta: Path) -> "pd.DataFrame":
    """Uma linha por frame e anotador: vídeo, local, tempo e código original."""
    raise NotImplementedError("Fase 0")


def ler_metc(pasta: Path) -> "pd.DataFrame":
    """Uma linha por frame: vídeo, tempo e código original."""
    raise NotImplementedError("Fase 0")


def votar_maioria(anotacoes: "pd.DataFrame") -> "pd.DataFrame":
    """Um rótulo por frame quando mais da metade dos anotadores concorda."""
    raise NotImplementedError("Fase 1")


def descartar_trocas(rotulos: "pd.DataFrame", margem_s: float = MARGEM_TROCA_S) -> "pd.DataFrame":
    """Remove os frames a menos de ``margem_s`` de cada troca de movimento."""
    raise NotImplementedError("Fase 1")
