# INC-002 — Métrica de receita inconsistente

**Sistema:** mini_orders_pipeline
**Severidade inicial:** média

## Sintoma
O dashboard de receita diária exibiu valores inconsistentes depois da carga de pedidos do parceiro `mobile_app`.

## Mensagem observada
Alguns registros chegaram com `order_total` como string usando vírgula decimal, por exemplo `"59,90"`.

## Impacto
A transformação não falhou imediatamente, mas produziu métrica incorreta em parte dos registros.
