# INC-001 — Falha na ingestão de pedidos

**Sistema:** mini_orders_pipeline
**Severidade inicial:** alta
**Reportado por:** monitoramento de pipeline

## Sintoma
O job `orders_daily_ingestion` falhou durante a etapa de ingestão de pedidos. O erro começou após a entrada de um novo lote enviado pelo parceiro `marketplace_beta`.

## Mensagem observada
`KeyError: 'customer_id'`

## Impacto
Pedidos do parceiro não foram processados na janela esperada. O dashboard diário de receita ficou incompleto.

## Pedido ao sistema agêntico
Investigar a causa provável, consultar evidências externas e apontar quais módulos do projeto-alvo podem precisar de alteração.
