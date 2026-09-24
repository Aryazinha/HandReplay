"""Regras da Fase 3: suavização, trechos, status, mapa, nota, faixa e frases.

Esqueleto, implementado na Fase 3.

Núcleo puro: sem I/O e sem estado. Recebe probabilidades (ou tempos por passo) e devolve números
e objetos do contrato. É usado pela API e pelas métricas do produto, que passam as anotações
humanas "pelas mesmas regras". Os cinco casos fixos do plano estão em tests/test_regras.py.

    nota = arredondar(100 x P x D)
    P = média, nos 6 passos, de min(tempo do passo / 2 s; 1)
    D = min(duração / 40 s; 1)

Dependências permitidas: numpy, ``handreplay.contrato`` e ``handreplay.textos``.
"""

from collections.abc import Sequence

import numpy as np

from handreplay.contrato import FraseCard, Orientacao, Resultado

VERSAO_REGRAS = "1.0.0"

JANELA_SUAVIZACAO_S = 1.0
TRECHO_MINIMO_S = 1.0
LIMIAR_CONFIANCA = 0.60
DURACAO_MINIMA_OMS_S = 40.0


def calcular_nota(tempos_s: Sequence[float], duracao_s: float) -> int:
    """Nota de 0 a 100 a partir do tempo de cada um dos 6 passos e da duração do vídeo."""
    raise NotImplementedError("Fase 3")


def exigir_lavagem(tempos_s: Sequence[float]) -> None:
    """Levanta ``ErroAnalise('sem_lavagem')`` se nenhum passo somar 2 s."""
    raise NotImplementedError("Fase 3")


def frase_tela(tempos_s: Sequence[float], duracao_s: float) -> str:
    """Frase principal da tela Analisar ("Faltou ..., e ... ficou curto.")."""
    raise NotImplementedError("Fase 3")


def frase_card(tempos_s: Sequence[float], duracao_s: float) -> FraseCard:
    """Frase do card pela primeira regra aplicável da Fase 6, com o trecho em destaque."""
    raise NotImplementedError("Fase 3")


def montar_resultado(
    probabilidades: np.ndarray,
    *,
    fps: float,
    duracao_s: float,
    orientacao: Orientacao,
    versao_modelo: str,
) -> Resultado:
    """Aplica todas as regras a uma matriz (frames x 7) de probabilidades calibradas."""
    raise NotImplementedError("Fase 3")
