# HIST-014 — Schema drift no parceiro marketplace_beta

Em 2026-06-21, o parceiro `marketplace_beta` enviou lote com campo `buyer_id` no lugar de `customer_id`. O incidente foi resolvido temporariamente com reprocessamento manual.

A recomendação pós-incidente foi adicionar validação explícita de campos obrigatórios e mensagens de erro estruturadas antes da transformação.
