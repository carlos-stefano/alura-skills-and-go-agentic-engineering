# Runbook — Datas em pipelines de pedidos

Campos de data em pedidos devem ser normalizados antes da camada analítica.

## Padrão preferencial
O formato preferencial para `created_at` é ISO-8601, por exemplo: `2026-07-08T10:00:00Z`.

## Variações conhecidas
Parceiros regionais podem enviar datas como `DD/MM/YYYY HH:MM:SS`. Esse formato deve ser tratado explicitamente ou bloqueado com erro descritivo.

## Conduta recomendada
1. Identificar se o erro ocorre na validação ou na transformação.
2. Localizar o módulo que interpreta datas.
3. Propor uma validação ou normalização antes da transformação final.
4. Exigir testes cobrindo ISO-8601 e formatos alternativos aceitos.
