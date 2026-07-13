# mini_orders_pipeline

Este é o projeto-base usado na Aula 2 para análise de incidentes com agentes.

Você vai trabalhar com um pipeline simplificado de pedidos de e-commerce, identificando falhas, rastreando impacto entre módulos e propondo correções.

## Visão geral do fluxo

1. `ingestao_pedidos.py`: recebe registros brutos.
2. `validacao_schema.py`: valida campos obrigatórios e estrutura esperada.
3. `transformacao_pedidos.py`: normaliza dados e calcula campos derivados.
4. `notificacao_falhas.py`: prepara mensagens de erro para acompanhamento.

## Como explorar o projeto

- Código-fonte: `src/mini_orders_pipeline/`
- Testes: `tests/`
- Amostras de entrada: `data_samples/`

Sugestão de leitura:

1. Entenda o fluxo de ponta a ponta pelos módulos em `src`.
2. Rode os testes para observar o comportamento esperado.
3. Use os arquivos de `data_samples` para reproduzir cenários de erro e validar hipóteses.

## Escopo

O projeto foi intencionalmente reduzido para facilitar investigação e experimentação.

Em outras palavras: ele prioriza clareza de raciocínio sobre cobertura completa de casos de produção.
