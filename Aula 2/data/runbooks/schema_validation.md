# Runbook — Validação de schema em pipelines de pedidos

Antes de transformar pedidos, o pipeline deve validar campos obrigatórios.

Campos obrigatórios esperados:

- `order_id`: string não vazia
- `customer_id`: string não vazia
- `order_total`: número positivo
- `created_at`: string em formato ISO-8601
- `items`: lista não vazia de itens

## Procedimento recomendado

1. Validar presença dos campos obrigatórios antes de acessar chaves diretamente.
2. Separar registros inválidos para quarentena ou erro estruturado.
3. Registrar no log o campo ausente, o parceiro e o identificador do pedido.
4. Evitar que a transformação lance `KeyError` genérico sem contexto.

## Critério de escalonamento

Escalar para engenharia quando a falha indicar alteração de contrato de dados por parceiro externo ou quando mais de 1% dos registros de um lote forem inválidos.
