"""Os cinco casos fixos da Fase 3 do plano para a nota, a faixa e as frases.

Até a Fase 3, as regras levantam NotImplementedError e estes testes ficam como xfail estrito.
Quando as regras forem implementadas, os testes passam, o pytest acusa XPASS e o marcador abaixo
tem que ser removido.
"""

import pytest

from handreplay import regras
from handreplay.contrato import ErroAnalise, faixa_da_nota

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="regras implementadas na Fase 3"
)

# Tempos dos 6 passos, em segundos, na ordem 1 a 6.
COMPLETA = (6.0, 6.0, 6.0, 6.0, 6.0, 6.0)


def test_exemplo_dos_mockups() -> None:
    # Polegar pulado (passo 5) e dorso dos dedos em 1,1 s (passo 4), em 38 s.
    tempos = (7.2, 4.7, 4.8, 1.1, 0.0, 5.3)

    nota = regras.calcular_nota(tempos, duracao_s=38.0)

    assert nota == 72
    assert faixa_da_nota(nota) == "QUASE LÁ"
    assert regras.frase_card(tempos, duracao_s=38.0).texto == "Meus polegares ficaram de fora."


def test_lavagem_completa_de_45_s_da_100() -> None:
    assert regras.calcular_nota(COMPLETA, duracao_s=45.0) == 100


def test_lavagem_completa_de_30_s_da_75() -> None:
    assert regras.calcular_nota(COMPLETA, duracao_s=30.0) == 75


def test_um_passo_nao_detectado_em_50_s_da_83() -> None:
    tempos = (6.0, 6.0, 6.0, 6.0, 0.0, 6.0)

    assert regras.calcular_nota(tempos, duracao_s=50.0) == 83


def test_video_sem_lavagem_da_erro_sem_lavagem() -> None:
    tempos = (0.0, 1.0, 0.0, 0.0, 0.4, 0.0)

    with pytest.raises(ErroAnalise) as erro:
        regras.exigir_lavagem(tempos)

    assert erro.value.codigo == "sem_lavagem"
