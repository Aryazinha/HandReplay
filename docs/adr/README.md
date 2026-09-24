# Registros de decisão de arquitetura (ADRs)

Cada ADR registra uma decisão que muda a estrutura do projeto, o problema do plano que a motivou e o que foi descartado. O contexto completo está em [docs/architecture/diagnostico-e-proposta.md](../architecture/diagnostico-e-proposta.md).

| # | Decisão | Status |
|---|---|---|
| [0001](0001-monolito-nucleo-funcional.md) | Monólito pequeno com núcleo funcional e casca fina | Aceito |
| [0002](0002-separacao-offline-api-e-mesmo-preprocessamento.md) | Dois pacotes (offline × API) e o mesmo pré-processamento no treino e na API | Aceito |
| [0003](0003-contrato-json-versionado.md) | Contrato JSON versionado com Pydantic | Aceito |
| [0004](0004-servidor-sem-estado-card-no-navegador.md) | API sem estado e card gerado no navegador | Aceito |
| [0005](0005-hospedagem-custo-zero.md) | Hospedagem de custo zero: GitHub Pages + container portátil | Aceito |
| [0006](0006-pesos-e-exemplos-no-hf-hub.md) | Pesos e vídeos de exemplo em repositórios do HF Hub | Aceito |

Os antigos 0007 (mesmo pré-processamento) e 0008 (dependências e qualidade) não existem mais. O primeiro foi incorporado ao 0002, e o segundo virou a seção "Qualidade" do README.

## Modelo

```markdown
# ADR NNNN — Título curto

- **Status:** proposto | aceito | substituído por NNNN
- **Data:** DD/MM/AAAA

## Contexto
O problema concreto do plano e as restrições.

## Decisão
O que foi decidido, em frases diretas.

## Consequências
O que fica mais fácil, o que fica mais difícil e o que muda na estrutura.

## Alternativas consideradas
Cada alternativa e o motivo de não ter sido escolhida.
```
