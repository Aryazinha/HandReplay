"""A configuração vem só de variáveis de ambiente e recusa valores perigosos."""

from pathlib import Path

import pytest

from handreplay.config import carregar_config


def test_padroes_sem_variaveis() -> None:
    config = carregar_config({})

    assert config.dir_dados == Path("data")
    assert config.max_mb == 200
    assert config.max_bytes == 200 * 1024 * 1024
    assert config.max_duracao_s == 90
    assert config.threads == 2
    assert config.origens == ()
    assert config.porta == 8000


def test_origens_do_cors() -> None:
    config = carregar_config(
        {"HANDREPLAY_ORIGENS": "https://usuario.github.io/, http://localhost:5500"}
    )

    assert config.origens == ("https://usuario.github.io", "http://localhost:5500")


def test_origem_curinga_e_recusada() -> None:
    with pytest.raises(ValueError, match="HANDREPLAY_ORIGENS"):
        carregar_config({"HANDREPLAY_ORIGENS": "*"})


@pytest.mark.parametrize("valor", ["abc", "0", "-5"])
def test_limite_invalido_e_recusado(valor: str) -> None:
    with pytest.raises(ValueError, match="HANDREPLAY_MAX_MB"):
        carregar_config({"HANDREPLAY_MAX_MB": valor})
