# ADR 0005 — Hospedagem de custo zero: front no GitHub Pages e API em container portátil

- **Status:** aceito em 24/09/2026, com um ajuste: `GET /saude` só é chamado quando a pessoa abre o painel "Enviar vídeo"
- **Data:** 24/09/2026
- **Substitui:** a decisão de 23/09/2026 de publicar o app inteiro num Space Docker (revisão 1 do diagnóstico)

## Contexto

O plano prevê publicar o app "de graça" num Space Docker do Hugging Face. Duas coisas mudaram:

1. **Custo zero.** O projeto passa a aceitar só serviços gratuitos ou cobertos por benefício de estudante (GitHub Student Developer Pack, Azure for Students). Nada pode exigir pagamento nem cartão de crédito.
2. **O Space Docker deixou de ser gratuito para criar.** A documentação do Hugging Face diz hoje que "creating a new Space that runs on compute (Gradio or Docker) requires a paid plan" [H1][H2].

O app tem duas partes com necessidades diferentes:

- **Front:** HTML, CSS e JS estáticos, os 3 exemplos já calculados e o card gerado no navegador. Não precisa de servidor.
- **API:** `POST /analisar` com ffmpeg e ONNX Runtime em CPU. Recebe vídeos de até 200 MB e 90 s, e deve responder em até 30 s para um vídeo de 60 s (Fases 3 e 4).

## Decisão

1. **Front e API são publicados separadamente.**
   - O front vai para o **GitHub Pages**, junto com o JSON dos 3 exemplos. Os vídeos dos exemplos são baixados do HF Hub no deploy.
   - Sem a API, o front funciona em "modo só exemplos".
   - A URL da API fica em `app/js/config.js`; se estiver vazia, o front entra no modo só exemplos.
2. **A API roda num container portátil**, sem nada exclusivo de um provedor:
   - Dockerfile genérico, com a porta em `PORT` e usuário sem root.
   - Imagem pública no ghcr.io.
   - CORS feito na própria aplicação, aceitando só a origem do front.
   - Nenhum SDK nem arquivo de infraestrutura de um provedor no repositório.
3. **O provedor recomendado para a API é o Azure Container Apps**, no plano de consumo, pago pelo Azure for Students:
   - `minReplicas = 0`, para escalar a zero quando ninguém usa;
   - no máximo 2 vCPU e 4 GiB por réplica.
4. **O Heroku pelo Student Pack e o Space Docker ficam descartados** (comparação abaixo).

## Comparação dos provedores para a API

Cada número traz a fonte oficial ao lado. "Pendente" quer dizer que não encontrei o número em fonte oficial e que ele será medido na semana 5, em vez de ser suposto.

| Critério | Azure for Students + Azure Container Apps | Heroku pelo GitHub Student Pack | Space Docker numa conta antiga do HF |
|---|---|---|---|
| **Custo** | US$ 0. Crédito de US$ 100 [A1]. Além disso, o Container Apps dá de graça, por assinatura e por mês, 180.000 vCPU-s, 360.000 GiB-s e 2 milhões de requisições [A2]. Com zero réplicas, não há cobrança [A2]. | Crédito de US$ 13 por mês durante 24 meses [K1]. O que passar do crédito é cobrado no cartão [K1]. Eco custa US$ 5/mês; Basic, US$ 7/mês [K4]. | O hardware CPU Basic é "Free!", mas criar um Space Docker exige plano pago [H2]. O PRO custa US$ 9/mês [H3]. |
| **Exige cartão?** | Não: "No credit card required" [A1]. | Sim: "you will need a valid credit or debit card on file to redeem this offer" [K1]. | A conta gratuita não exige cartão, mas criar o Space exige plano pago [H1][H2]. |
| **Validade do benefício** | O crédito vale por 12 meses, com renovação anual "as long as you're a student". Só para "full-time university students". Se você não migrar para pagamento por uso, a assinatura é desativada no fim [A1]. | 24 meses; é preciso ter 18 anos ou mais [K1]. | Não se aplica. A documentação não prevê exceção para contas antigas [H1][H2]. O Space dorme após 48 h sem uso [H2]. |
| **Limite de upload** | Não documentado. **Pendente (medir na semana 5).** | Não documentado. **Pendente.** | Não documentado. **Pendente.** |
| **Tempo máximo por requisição** | 240 s ("Request time out is 240 seconds") [A3]. | 30 s, contados depois que o corpo inteiro da requisição chega ao dyno. Depois disso, cada byte trafegado renova uma janela de 55 s. Não é configurável [K2]. | Não documentado. **Pendente.** |
| **Cold start** | Com zero réplicas, a primeira requisição dispara um cold start [A5]. A réplica volta a zero 300 s depois do último evento (cooldown) [A4]. A duração do cold start não é documentada: **pendente**. | O dyno Eco dorme após 30 min sem tráfego e acorda "after a short delay", sem número [K3]. **Pendente.** | O Space dorme após 48 h e reinicia quando alguém visita [H2]. A duração não é documentada: **pendente**. |
| **Recursos por instância** | Até 2 vCPU e 4 GiB num ambiente só de consumo [A6]. | 0,5 GB de RAM, Eco ou Basic [K4]. | 2 vCPU e 16 GB [H2]. |
| **Portabilidade** | Aceita qualquer imagem `linux/amd64` de registro público ou privado [A6]. | Não avaliada, porque o Heroku foi descartado pelo cartão. | Exige cabeçalho YAML no README e a porta configurada no Space. |

### Por que o Azure Container Apps

- **É a única opção sem cartão e sem pagamento.**
  - O Heroku viola a restrição de cartão.
  - O Space Docker viola a restrição de pagamento. A documentação oficial exige plano pago para criar e não menciona exceção para contas antigas. Que uma conta antiga consiga criar é algo que só uma tentativa confirmaria (P16 no diagnóstico).
- **O limite de 240 s cobre a meta de 30 s com folga.**
  - No Heroku, a resposta teria de sair em até 30 s depois do fim do upload, ou seja, exatamente a meta do plano, sem margem.
  - Os 0,5 GB de RAM do Heroku também ficam apertados para frames de 90 s mais o modelo.
- **Com 2 vCPU e 4 GiB,** o hardware fica próximo das 2 vCPU que o plano previa no Spaces.

### Estimativa de consumo dentro da cota gratuita

Esta é uma conta minha, feita com os números oficiais, e não um número publicado pela Microsoft.

- **Só quem abre o painel "Enviar vídeo" consome a cota.**
  - A página carrega os exemplos só do GitHub Pages e não faz nenhuma requisição à API.
  - A primeira chamada à API é o `GET /saude`, feito quando o painel é aberto.
  - Uma visita que só vê os exemplos custa **zero** na API: nenhuma réplica sobe e nenhuma requisição é contada.
- **Premissas:**
  - Com `minReplicas = 0`, a réplica não tem direito à tarifa reduzida de ociosidade [A2]. Por isso, conta como ativa até o fim do cooldown de 300 s [A4].
  - Uma abertura do painel seguida de uma análise mantém uma réplica de 2 vCPU e 4 GiB ligada por cerca de 300 s + 30 s = 330 s.
  - Abrir o painel e desistir de enviar custa quase o mesmo, cerca de 300 s de réplica ligada.
- **Consumo por abertura do painel com análise:** 660 vCPU-s e 1.320 GiB-s.
- **Resultado:** a cota mensal cobre cerca de **270 aberturas do painel "Enviar vídeo" por mês** (180.000 ÷ 660 ≈ 272; 360.000 ÷ 1.320 ≈ 272), qualquer que seja o número de visitas que só veem os exemplos.
  - Várias aberturas dentro da mesma janela de 5 minutos dividem a mesma réplica, então o número real tende a ser maior.
  - Acima disso, o consumo sai do crédito de US$ 100.
  - Com 1 vCPU e 2 GiB, a cota cobriria o dobro, mas a meta de 30 s ainda precisa ser medida nessa configuração.
- **Confirmar na semana 5:** o `maxReplicas` que limita o gasto (P11) e o destino dos logs (P15).

## Front: GitHub Pages

- **Custo:** zero em repositório público. O GitHub Free oferece "GitHub Pages in public repositories" [G1], e o Actions é gratuito em repositórios públicos com os runners padrão [G2].
- **Limites:**
  - site de até 1 GB;
  - limite *soft* de banda de 100 GB/mês;
  - deploy com timeout de 10 min [G3].
  - Três vídeos de exemplo cabem com folga nesses limites.
- **Por que um workflow:** publicar a partir de uma branch só aceita a raiz do repositório ou `/docs` [G4]. Por isso, o deploy usa um workflow de Actions (`.github/workflows/pages.yml`, Fase 5) que:
  1. copia `app/`;
  2. baixa os 3 vídeos do HF Hub no commit fixado e confere o checksum;
  3. publica o resultado com `actions/upload-pages-artifact` e `actions/deploy-pages` [G4].
- **Os vídeos nunca entram no git,** e o site fica todo na mesma origem, sem depender de o HF Hub servir vídeo para outra origem.
- **Plano B:** um Space estático do HF, que é "free for everyone" [H1], ao custo de manter um segundo repositório.

## Imagem da API: ghcr.io

- O GitHub Packages "is free for public packages", e o armazenamento e a banda do Container registry são hoje gratuitos [G5].
- O Container Apps baixa imagens de qualquer registro público [A6], então não é preciso um Azure Container Registry, que é pago.
- A imagem é construída no PC com Docker, que já está instalado.

## Consequências

- **Positivas:**
  - Custo zero, sem cartão.
  - O front público continua no ar mesmo quando o benefício de estudante acabar ou a API cair.
  - Trocar de provedor é só apontar outra URL em `app/js/config.js` e configurar CORS e `PORT` no novo lugar.
- **Negativas:**
  - Duas publicações para manter. Por isso, a ordem de publicação do contrato fica definida: a API sai primeiro, depois o front (diagnóstico, seção 7.5).
  - O cold start aparece para quem abre o painel "Enviar vídeo" com a API dormindo. Nesse momento, o front chama `GET /saude` e mostra o estado "servidor acordando" enquanto a pessoa lê as orientações. Essa rota foi aprovada (A1) como exceção ao "Não há outra rota" do plano.
  - O benefício do Azure depende de você ser estudante universitário em tempo integral (P1). Sem ele, a API roda só localmente (`docker run`), e o site público fica no modo só exemplos.
- **O que muda na estrutura:**
  - Sai o cabeçalho YAML do Spaces.
  - Entram `HANDREPLAY_ORIGENS`, `HANDREPLAY_THREADS` e `PORT`; saem `CPU_CORES` e `HANDREPLAY_EXEMPLOS`.
  - A API deixa de servir `app/`.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| Heroku pelo Student Pack | Exige cartão [K1]; 30 s por requisição [K2]; 0,5 GB de RAM [K4]. |
| Space Docker (conta nova ou antiga) | Criar exige plano pago [H1][H2]. |
| Front servido pela API | O front sumiria junto com a API; o pedido exige um front que funcione sem back-end. |
| Space estático para o front | É viável e fica como plano B, mas exige um segundo repositório [H1]. |
| Inferência no navegador para dispensar a API | Adiada pela observação 21 do plano; não é antecipada. |

## Pendências ligadas a este ADR

Os números remetem à seção 11 do [diagnóstico](../architecture/diagnostico-e-proposta.md).

| # | Pendência | Quando |
|---|---|---|
| P1 | Elegibilidade ao Azure for Students | Antes da semana 5 |
| P2 | Limite de upload no ingress do Container Apps | Medir na semana 5 |
| P11 | `maxReplicas` e concorrência | Semana 5 |
| P13 | Duração do cold start e tempo de espera do front | Medir na semana 5 |
| P15 | Destino dos logs e regiões permitidas para estudantes. A intenção é criar o ambiente sem Log Analytics, se o provedor permitir. | Semana 5 |
| P16 | Se uma conta antiga do HF ainda cria Space Docker gratuito | Só se o Azure falhar |

## Fontes

- [A1] Azure for Students: <https://azure.microsoft.com/en-us/free/students/>
- [A2] Azure Container Apps, *Billing*: <https://learn.microsoft.com/en-us/azure/container-apps/billing>
- [A3] Azure Container Apps, *Ingress overview*: <https://learn.microsoft.com/en-us/azure/container-apps/ingress-overview>
- [A4] Azure Container Apps, *Scaling* (tabela "Scale behavior": cooldown de 300 s): <https://learn.microsoft.com/en-us/azure/container-apps/scale-app>
- [A5] Azure Container Apps, *Reducing cold-start time*: <https://learn.microsoft.com/en-us/azure/container-apps/cold-start>
- [A6] Azure Container Apps, *Containers* (combinações de vCPU e memória; registros): <https://learn.microsoft.com/en-us/azure/container-apps/containers>
- [K1] Heroku, *GitHub Student Developer Pack Offer*: <https://www.heroku.com/github-students/>
- [K2] Heroku Dev Center, *Request Timeout*: <https://devcenter.heroku.com/articles/request-timeout>
- [K3] Heroku Dev Center, *Eco Dyno Hours*: <https://devcenter.heroku.com/articles/eco-dyno-hours>
- [K4] Heroku Dev Center, *Dyno Types*: <https://devcenter.heroku.com/articles/dyno-types>
- [H1] Hugging Face, *Spaces Overview*: <https://huggingface.co/docs/hub/spaces-overview>
- [H2] Hugging Face, *Using GPU Spaces* (tabela de CPU, nota sobre plano pago, suspensão após 48 h): <https://huggingface.co/docs/hub/spaces-gpus>
- [H3] Hugging Face, *PRO*: <https://huggingface.co/pro>
- [G1] GitHub, *GitHub's plans*: <https://docs.github.com/en/get-started/learning-about-github/githubs-plans>
- [G2] GitHub, *GitHub Actions billing*: <https://docs.github.com/en/billing/concepts/product-billing/github-actions>
- [G3] GitHub, *GitHub Pages limits*: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>
- [G4] GitHub, *Configuring a publishing source for your GitHub Pages site*: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
- [G5] GitHub, *GitHub Packages billing*: <https://docs.github.com/en/billing/concepts/product-billing/github-packages>
