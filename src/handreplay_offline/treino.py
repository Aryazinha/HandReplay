"""Treino da Fase 2, no Kaggle: fine-tuning da MobileNetV2 e calibração da confiança.

Esqueleto, implementado na Fase 2.

- MobileNetV2 pré-treinada no ImageNet, com 7 saídas na ordem de
  ``handreplay.contrato.CLASSES_MODELO``.
- Perda ponderada pelo desbalanceamento; no máximo três rodadas; fica a de maior F1 macro
  na validação.
- Augmentation no treino: recorte aleatório 224 x 224, rotação de até 15 graus, brilho, contraste
  e cor, desfoque leve e espelhamento horizontal. Validação e teste usam
  ``handreplay.video.preparar_entrada`` (o mesmo recorte central da API).
- Temperature scaling na validação.
- Reprodutibilidade conforme a nota oficial do PyTorch: ``torch.manual_seed``,
  ``cudnn.benchmark = False``, ``use_deterministic_algorithms(True)``, ``seed_worker`` e um
  ``torch.Generator`` no ``DataLoader``.

Dependências permitidas: torch, torchvision, ``sementes``, ``handreplay.contrato`` e
``handreplay.video``.
"""

from handreplay_offline.sementes import SEMENTE


def fixar_sementes_torch(semente: int = SEMENTE) -> None:
    """Fixa as sementes do Python, do NumPy e do torch, e liga os algoritmos determinísticos."""
    raise NotImplementedError("Fase 2")


def seed_worker(worker_id: int) -> None:
    """``worker_init_fn`` do ``DataLoader``, conforme a nota de reprodutibilidade do PyTorch."""
    raise NotImplementedError("Fase 2")


def treinar(rodada: int, semente: int = SEMENTE) -> None:
    """Uma rodada completa de treino; salva o checkpoint na saída do notebook."""
    raise NotImplementedError("Fase 2")


def calibrar_temperatura() -> float:
    """Ajusta a temperatura T na validação, minimizando a perda logarítmica."""
    raise NotImplementedError("Fase 2")
