"""Semente única do projeto e fixação dos geradores de números aleatórios fora do torch.

A semente do torch (``torch.manual_seed``, ``DataLoader`` com ``seed_worker``) fica em
``treino``: se ficasse aqui, a preparação de dados passaria a depender de torch.

Dependências permitidas: numpy e a biblioteca padrão.
"""

import random

import numpy as np

SEMENTE = 42


def fixar_sementes(semente: int = SEMENTE) -> None:
    """Fixa os geradores globais do ``random`` e do NumPy."""
    random.seed(semente)
    np.random.seed(semente)


def gerador(semente: int = SEMENTE) -> np.random.Generator:
    """Gerador independente, usado por exemplo na divisão treino/validação (85/15) da Fase 1."""
    return np.random.default_rng(semente)
