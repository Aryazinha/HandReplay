"""Código que roda fora da API: PC local (Fases 0, 1 e 3) e Kaggle (Fase 2).

Nunca entra na imagem Docker e pode importar ``handreplay``, mas o contrário é proibido
(import-linter, contrato 1). Só ``treino`` e ``exportacao`` podem importar torch (contrato 3).
"""
