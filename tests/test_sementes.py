"""A mesma semente reproduz as mesmas sequências aleatórias fora do torch."""

import random

import numpy as np

from handreplay_offline.sementes import SEMENTE, fixar_sementes, gerador


def _sortear() -> tuple[float, list[float]]:
    return random.random(), np.random.rand(3).tolist()


def test_fixar_sementes_repete_as_sequencias() -> None:
    fixar_sementes()
    primeira = _sortear()
    fixar_sementes()

    assert _sortear() == primeira


def test_gerador_da_divisao_e_reprodutivel() -> None:
    videos = [f"video_{i:03d}" for i in range(20)]

    assert gerador().permutation(videos).tolist() == gerador(SEMENTE).permutation(videos).tolist()
