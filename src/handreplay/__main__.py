"""Linha de comando: ``python -m handreplay video.mp4 [--saida resultado.json]``.

Esqueleto, implementado na Fase 3.

Gera o JSON de um vídeo (critério de pronto da Fase 3) e o JSON dos 3 exemplos em
app/exemplos/ (Fase 7). Em caso de erro previsto, escreve a ``RespostaErro`` e sai com código 1.

Dependências permitidas: config, contrato, modelo e pipeline.
"""

import argparse
import sys


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m handreplay", description="Analisa um vídeo de lavagem de mãos."
    )
    parser.add_argument("video", help="caminho do vídeo (mp4, mov ou webm)")
    parser.add_argument("--saida", help="arquivo JSON de saída; sem ele, imprime na tela")
    return parser


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError("Fase 3")


if __name__ == "__main__":
    sys.exit(main())
