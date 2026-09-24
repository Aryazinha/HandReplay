# data/

Esta pasta nunca vai para o git; o único arquivo versionado é este README. Nela ficam os datasets de terceiros, os frames extraídos, os vídeos gravados com celular e o `.onnx` local.

**Aponte `HANDREPLAY_DADOS` para uma pasta fora do OneDrive.** A Fase 1 ocupa de 30 a 50 GB, e uma pasta sincronizada enviaria tudo isso para a nuvem. Veja o `.env.example`.

## Organização esperada

| Pasta | Conteúdo | Fase |
|---|---|---|
| `brutos/pskus/` | Arquivos do PSKUS baixados do Zenodo (começando pelo `DataSet4.zip`) | 0–1 |
| `brutos/metc/` | Subconjunto METC baixado do Zenodo | 0–1 |
| `frames/` | Frames a 5 fps, lado menor com 224 px, extraídos com o mesmo filtro ffmpeg da API | 1 |
| `indice/` | `indice.csv` (frame, rótulo, vídeo, local, divisão) e o gráfico das classes | 1 |
| `celular/` | Os 18 vídeos gravados com celular e a planilha de anotação. São dados de pessoas: nunca publicar, só as métricas. | 3 |
| `modelo/handreplay.onnx` | Cópia local do modelo exportado no Kaggle | 2 |
| `exemplos/` | Cópia local dos 3 vídeos de exemplo, que ficam publicados no HF Hub | 7 |

## Licenças dos dados

- **PSKUS** (<https://zenodo.org/records/4537209>): CC BY-SA 4.0.
- **METC** (<https://zenodo.org/records/5808789>): CC BY 4.0.

Qualquer dado recebido pelos pedidos de 22/09/2026 também fica aqui, com as condições de uso registradas no README principal.
