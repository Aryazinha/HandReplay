"""O contrato v1 aceita o exemplo dos mockups e recusa resultados incoerentes."""

import copy
import json
from collections.abc import Callable
from pathlib import Path
from typing import get_args

import pytest
from pydantic import ValidationError

from handreplay.contrato import (
    CLASSES_MODELO,
    REGIOES,
    STATUS_HTTP,
    VERSAO_CONTRATO,
    CodigoErro,
    Regioes,
    RespostaErro,
    Resultado,
    faixa_da_nota,
)

EXEMPLO_72 = Path(__file__).parent / "dados" / "resultado_exemplo_72.json"


@pytest.fixture
def exemplo() -> dict:
    return json.loads(EXEMPLO_72.read_text(encoding="utf-8"))


def test_exemplo_dos_mockups_e_valido(exemplo: dict) -> None:
    resultado = Resultado.model_validate(exemplo)

    assert resultado.nota == 72
    assert resultado.faixa == "QUASE LÁ"
    assert resultado.versao.contrato == VERSAO_CONTRATO
    assert resultado.model_dump(mode="json") == exemplo


def _campo_extra(r: dict) -> None:
    r["campo_novo"] = 1


def _faixa_errada(r: dict) -> None:
    r["faixa"] = "MUITO BEM"


def _cinco_passos(r: dict) -> None:
    r["passos"].pop()


def _passos_fora_de_ordem(r: dict) -> None:
    r["passos"][0], r["passos"][1] = r["passos"][1], r["passos"][0]


def _status_incoerente(r: dict) -> None:
    r["passos"][3]["status"] = "feito"


def _buraco_entre_trechos(r: dict) -> None:
    r["trechos"][2]["inicio_s"] = 10.6


def _trechos_nao_cobrem_o_video(r: dict) -> None:
    r["duracao_s"] = 45.0


def _tempo_diferente_dos_trechos(r: dict) -> None:
    r["passos"][0]["tempo_s"] = 6.0


def _destaque_fora_do_texto(r: dict) -> None:
    r["frase_card"]["destaque"] = "palmas"


def _regiao_faltando(r: dict) -> None:
    del r["regioes"]["polegares"]


def _classe_invalida(r: dict) -> None:
    r["trechos"][1]["classe"] = 7


def _confianca_acima_de_1(r: dict) -> None:
    r["trechos"][1]["confianca"] = 1.2


def _passos_completos_errado(r: dict) -> None:
    r["resumo"]["passos_completos"] = 5


def _passo_mais_longo_errado(r: dict) -> None:
    r["resumo"]["passo_mais_longo"] = {"numero": 6, "tempo_s": 5.3}


@pytest.mark.parametrize(
    "estragar",
    [
        _campo_extra,
        _faixa_errada,
        _cinco_passos,
        _passos_fora_de_ordem,
        _status_incoerente,
        _buraco_entre_trechos,
        _trechos_nao_cobrem_o_video,
        _tempo_diferente_dos_trechos,
        _destaque_fora_do_texto,
        _regiao_faltando,
        _classe_invalida,
        _confianca_acima_de_1,
        _passos_completos_errado,
        _passo_mais_longo_errado,
    ],
)
def test_resultado_incoerente_e_recusado(exemplo: dict, estragar: Callable[[dict], None]) -> None:
    resultado = copy.deepcopy(exemplo)
    estragar(resultado)

    with pytest.raises(ValidationError):
        Resultado.model_validate(resultado)


@pytest.mark.parametrize(
    ("nota", "faixa"),
    [
        (100, "MUITO BEM"),
        (90, "MUITO BEM"),
        (89, "QUASE LÁ"),
        (60, "QUASE LÁ"),
        (59, "VAMOS DE NOVO"),
        (0, "VAMOS DE NOVO"),
    ],
)
def test_faixas_da_nota(nota: int, faixa: str) -> None:
    assert faixa_da_nota(nota) == faixa


def test_resposta_de_erro_valida(exemplo: dict) -> None:
    erro = RespostaErro.model_validate(
        {
            "versao": exemplo["versao"],
            "erro": {
                "codigo": "sem_lavagem",
                "mensagem": "Não reconhecemos uma lavagem de mãos neste vídeo.",
            },
        }
    )

    assert STATUS_HTTP[erro.erro.codigo] == 422


def test_codigo_de_erro_fora_do_contrato_e_recusado(exemplo: dict) -> None:
    with pytest.raises(ValidationError):
        RespostaErro.model_validate(
            {"versao": exemplo["versao"], "erro": {"codigo": "erro_interno", "mensagem": "x"}}
        )


def test_todo_codigo_de_erro_tem_status_http_4xx() -> None:
    assert set(STATUS_HTTP) == set(get_args(CodigoErro))
    assert all(400 <= status < 500 for status in STATUS_HTTP.values())


def test_ordem_das_classes_do_modelo() -> None:
    assert CLASSES_MODELO == ("outro", 1, 2, 3, 4, 5, 6)


def test_regioes_do_json_batem_com_o_modelo() -> None:
    assert tuple(Regioes.model_fields) == REGIOES
