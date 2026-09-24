"""Configuração lida só de variáveis de ambiente (documentadas em .env.example).

Nenhum valor secreto fica no código, e nenhuma variável é exclusiva de um provedor: a mesma
imagem roda no PC, no Azure Container Apps ou em qualquer outro host de containers (ADR 0005).

Dependências permitidas: só a biblioteca padrão.
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

_PADROES = {
    "HANDREPLAY_DADOS": "./data",
    "HANDREPLAY_MODELO": "./data/modelo/handreplay.onnx",
    "HANDREPLAY_MAX_MB": "200",
    "HANDREPLAY_MAX_DURACAO_S": "90",
    "HANDREPLAY_THREADS": "2",
    "HANDREPLAY_ORIGENS": "",
    "PORT": "8000",
}


@dataclass(frozen=True)
class Config:
    dir_dados: Path
    caminho_modelo: Path
    max_mb: int
    max_duracao_s: float
    threads: int
    origens: tuple[str, ...]
    porta: int

    @property
    def max_bytes(self) -> int:
        return self.max_mb * 1024 * 1024


def carregar_config(ambiente: Mapping[str, str] | None = None) -> Config:
    """Monta a configuração a partir de ``ambiente`` (por padrão, ``os.environ``)."""
    env = os.environ if ambiente is None else ambiente

    def valor(nome: str) -> str:
        return env.get(nome, "").strip() or _PADROES[nome]

    return Config(
        dir_dados=Path(valor("HANDREPLAY_DADOS")),
        caminho_modelo=Path(valor("HANDREPLAY_MODELO")),
        max_mb=_inteiro_positivo("HANDREPLAY_MAX_MB", valor("HANDREPLAY_MAX_MB")),
        max_duracao_s=float(
            _inteiro_positivo("HANDREPLAY_MAX_DURACAO_S", valor("HANDREPLAY_MAX_DURACAO_S"))
        ),
        threads=_inteiro_positivo("HANDREPLAY_THREADS", valor("HANDREPLAY_THREADS")),
        origens=_origens(env.get("HANDREPLAY_ORIGENS", "")),
        porta=_inteiro_positivo("PORT", valor("PORT")),
    )


def _inteiro_positivo(nome: str, texto: str) -> int:
    try:
        numero = int(texto)
    except ValueError:
        raise ValueError(f"{nome} precisa ser um inteiro, recebeu {texto!r}") from None
    if numero <= 0:
        raise ValueError(f"{nome} precisa ser maior que zero, recebeu {numero}")
    return numero


def _origens(texto: str) -> tuple[str, ...]:
    """Lista de origens do CORS. ``*`` é recusado: a API só aceita a origem do front."""
    origens = tuple(o.strip().rstrip("/") for o in texto.split(",") if o.strip())
    if "*" in origens:
        raise ValueError("HANDREPLAY_ORIGENS não aceita '*'; informe a origem do front")
    return origens
