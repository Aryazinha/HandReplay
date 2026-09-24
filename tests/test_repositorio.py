"""Regras do repositório que protegem a imagem de produção e os dados de terceiros."""

import importlib
import json
import pkgutil
import re
import sys
from pathlib import Path

import handreplay
from handreplay.contrato import Resultado

RAIZ = Path(__file__).resolve().parents[1]
PROIBIDOS_NA_PRODUCAO = {"torch", "torchvision", "torchaudio", "pandas", "matplotlib"}


def _pacotes_de(requirements: Path) -> dict[str, str]:
    pacotes = {}
    for linha in requirements.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()
        if linha and not linha.startswith("-"):
            nome = re.split(r"[=<>!~\[; ]", linha, maxsplit=1)[0]
            pacotes[nome.lower()] = linha
    return pacotes


def test_producao_nao_tem_dependencias_de_treino() -> None:
    pacotes = _pacotes_de(RAIZ / "requirements.txt")

    assert not PROIBIDOS_NA_PRODUCAO & set(pacotes)


def test_producao_fixa_versoes_exatas() -> None:
    pacotes = _pacotes_de(RAIZ / "requirements.txt")

    assert pacotes
    assert all("==" in linha for linha in pacotes.values())


def test_todos_os_modulos_da_api_importam_sem_torch() -> None:
    for modulo in pkgutil.walk_packages(handreplay.__path__, prefix="handreplay."):
        importlib.import_module(modulo.name)

    assert "torch" not in sys.modules


def test_notebooks_sem_saidas() -> None:
    # Saídas de notebook podem conter frames dos datasets, que não podem ir para o git.
    for caminho in (RAIZ / "notebooks").glob("*.ipynb"):
        notebook = json.loads(caminho.read_text(encoding="utf-8"))
        for celula in notebook.get("cells", []):
            assert not celula.get("outputs"), f"{caminho.name} tem saídas; rode o nbstripout"


def test_exemplos_do_front_seguem_o_contrato() -> None:
    # Os JSON dos 3 exemplos (Fase 7) precisam seguir o contrato vigente antes de ir para o Pages.
    for caminho in (RAIZ / "app" / "exemplos").glob("*.json"):
        Resultado.model_validate_json(caminho.read_text(encoding="utf-8"))
