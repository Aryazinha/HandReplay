"""HandReplay: análise de um vídeo de lavagem de mãos segundo os 6 movimentos da OMS.

Este pacote contém tudo o que roda na API em CPU, mais o núcleo que o treino reaproveita
(contrato, regras e pré-processamento). Ele nunca importa torch; o código de treino fica em
``handreplay_offline``. Arquitetura: docs/architecture/diagnostico-e-proposta.md.
"""

__version__ = "0.1.0"
