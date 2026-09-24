"""Exportação do modelo calibrado para ONNX (Fase 2, no Kaggle).

Esqueleto, implementado na Fase 2.

- ``torch.onnx.export`` com ``dynamo=True``, o padrão desde o PyTorch 2.9, que exige onnx e
  onnxscript, e lote dinâmico via ``dynamic_shapes``.
- A saída já é ``softmax(logits / T)``: a API recebe probabilidades calibradas.
- Os metadados do .onnx registram a versão, a ordem das classes, a rodada e a semente.
- A paridade é conferida em 100 frames: ONNX Runtime e PyTorch recebem a mesma entrada de
  ``handreplay.video.preparar_entrada``.

Dependências permitidas: torch, onnx, onnxscript, onnxruntime, ``treino``, ``handreplay.contrato``
e ``handreplay.video``.
"""

from pathlib import Path


def exportar_onnx(destino: Path, temperatura: float, versao: str) -> None:
    """Exporta o melhor checkpoint com a temperatura embutida e os metadados."""
    raise NotImplementedError("Fase 2")


def verificar_paridade(caminho_onnx: Path, n_frames: int = 100) -> float:
    """Maior diferença absoluta entre as saídas do PyTorch e do ONNX Runtime."""
    raise NotImplementedError("Fase 2")
