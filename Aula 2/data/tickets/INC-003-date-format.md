# INC-003 — Falha ao transformar pedidos com created_at em formato brasileiro

## Resumo
O pipeline `mini_orders_pipeline` falhou ao processar pedidos recebidos de um parceiro regional.

## Sintoma observado
A etapa de transformação retorna erro ao interpretar o campo `created_at` quando o valor chega como `08/07/2026 10:00:00`.

## Impacto
Pedidos do parceiro regional ficam retidos antes da geração da base analítica diária.

## Evidência inicial
O erro aparece após a validação de schema, durante a transformação dos pedidos.

## Resultado esperado
O sistema deve identificar a causa provável, mapear o módulo afetado e propor uma correção conceitual sem alterar código automaticamente.
