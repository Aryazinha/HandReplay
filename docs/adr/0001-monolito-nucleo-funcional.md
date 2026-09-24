# ADR 0001 — Monólito pequeno com núcleo funcional e casca fina

- **Status:** aceito
- **Data:** 24/09/2026

## Contexto

O HandReplay tem um único contexto de negócio: analisar um vídeo de lavagem de mãos. O projeto tem um desenvolvedor, cerca de 72 horas e 8 fases. O plano exige que:

- as regras e a nota tenham cinco testes fixos (Fase 3, observação 16b);
- as métricas do produto passem as anotações humanas "pelas mesmas regras" do app (Fase 3);
- a função `analisar(video) -> dict` gere o JSON validado (Fases 3 e 4).

## Decisão

- **Núcleo puro**, sem I/O e sem estado: `contrato`, `textos` e `regras`. Recebe números e devolve números ou objetos do contrato.
- **Casca de I/O:** `video` (ffprobe e ffmpeg por subprocess) e `modelo` (ONNX Runtime), como módulos simples, sem interfaces abstratas.
- **Orquestração:** `pipeline.analisar(video, modelo, config)`. O modelo entra como parâmetro, carregado uma vez por processo e fácil de trocar nos testes.
- **Pontos de entrada:** `api` (FastAPI) e `__main__` (linha de comando).
- **A direção das dependências** (`api | __main__` → `pipeline` → `regras | video | modelo | config` → `textos` → `contrato`) é verificada pelo import-linter (contrato 4).

## Consequências

- As regras são testadas sem vídeo e sem modelo, e as métricas do produto reaproveitam as mesmas funções.
- Não há interfaces, camada de serviço, repositórios nem injeção de dependência para manter.
- Se aparecer um segundo adaptador real, por exemplo outro motor de inferência em Python, a extração de uma interface fica para esse momento.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Camadas (apresentação, serviço, domínio, persistência) | Não há persistência, e a camada de serviço só repassaria a chamada para `analisar`. |
| Hexagonal (portas e adaptadores) | Cada porta teria um único adaptador na v1; o núcleo puro já dá a testabilidade. |
| Monólito modular com fachadas por contexto | Há um único contexto. Só a fronteira offline × API importa, e ela está no ADR 0002. |
