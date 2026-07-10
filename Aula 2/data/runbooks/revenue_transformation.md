# Runbook — Transformação de receita

A função de transformação de pedidos deve normalizar `order_total` para número antes de calcular métricas de receita.

Casos conhecidos:

- Alguns parceiros enviam `order_total` como string com ponto decimal: `"59.90"`.
- Alguns parceiros legados enviam vírgula decimal: `"59,90"`.
- Valores inválidos devem ser rejeitados com erro estruturado.

A transformação não deve converter silenciosamente valores que não possam ser interpretados com segurança.
