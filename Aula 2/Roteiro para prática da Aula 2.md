# Aula 2 - Guia pratico para alunos (bloco de 3h)

## Formato da aula de hoje
Esta aula será dividida em exposição guiada + sprint prático.

1. Exposição guiada do Notebook 2A (agente único e ponte com aula anterior).
2. Exposição guiada de CrewAI (orquestração multiagente no Notebook 2B).
3. Exposição guiada introdutória de LangGraph (mesmo formalismo, contraste com CrewAI no Notebook 2C).
4. Sprint prático com foco principal no Notebook 2D (validação, limites e experimentação).

## Enfoque de cada notebook
- Notebook 2A: consolida a base de agente único, tool calling e leitura de evidências. É a ponte direta com a aula anterior (Notebook 1B).
- Notebook 2B (CrewAI): introduz decomposição de papéis e orquestração multiagente em formato de equipe. O objetivo é entender como a divisão de responsabilidades afeta qualidade e risco.
- Notebook 2C (LangGraph): mostra o mesmo problema com outro formalismo de orquestração (fluxo e estado explícitos). Serve para comparação arquitetural, não para aprofundamento completo neste bloco.
- Notebook 2D: concentra validação determinística, limites de autonomia e decisão final. É onde vocês praticam engenharia de qualidade do sistema, com intervenção técnica e comparação baseline vs variante, além de aprofundar na discussão entre um agente único vs multiagentes.

O Notebook 2D é o ponto em que análise probabilística (LLM) encontra critérios objetivos de aprovação/bloqueio, que é o núcleo de Agentic Engineering em produção.

## O que vocês vão entregar
Ao final do bloco, cada grupo entrega uma investigação técnica com:
- diagnóstico com evidências
- módulos afetados
- proposta conceitual de correção
- plano de testes
- decisão final (aprovar, aprovar com condições ou bloquear)

## Regras da atividade
1. Não inventem evidências.
2. Toda afirmação precisa apontar fonte consultada.
3. Não façam alteração automática de código.
4. Toda proposta precisa de plano de testes.
5. Revisão humana é obrigatória.

## Como organizar o grupo
Grupo de 3 a 4 pessoas.

Papeis sugeridos (rotacionem durante a aula):
1. Operação: executa células e registra resultados.
2. Auditoria: confere se há evidência para cada conclusão.
3. Qualidade: aponta risco, lacuna e contradição.
4. Relatoria (opcional): consolida a entrega final.

## Parte 1 - Exposicao guiada (acompanhem e anotem)

### Bloco 2A - Agente único
Foco da observação:
1. Como o agente decide usar tools.
2. Como ler trace e validar evidências.
3. Como ajustar prompt para reduzir resposta vaga.

Checkpoint rápido:
- Vocês conseguem explicar de onde veio cada conclusão mostrada.

### Bloco 2B - CrewAI
Foco da observação:
1. Como dividir responsabilidade entre papeis.
2. Como a orquestração sequencial muda a qualidade da saída.
3. Quais riscos surgem com multiagentes.

Checkpoint rápido:
- Vocês conseguem diferenciar o papel de cada agente.

### Bloco 2C - LangGraph (visao rapida)
Foco da observação:
1. Mesmo problema, formalismo diferente de orquestração.
2. Quando a estrutura explícita de fluxo ajuda.
3. Custo de complexidade vs ganho de previsibilidade.

Checkpoint rápido:
- Vocês conseguem comparar CrewAI e LangGraph em 2 criterios técnicos.

## Parte 2 - Sprint pratico (foco principal no Notebook 2D)

### Objetivo do sprint
Validar uma proposta com critérios determinísticos e produzir decisão técnica justificável.

### Tarefas obrigatorias
1. Rodar o fluxo do 2D e gerar saída final.
2. Validar a saída contra critérios objetivos:
   - evidências
   - módulos existentes
   - plano de testes
   - revisão humana
   - sem execução automática
3. Classificar a proposta: aprovar, aprovar com condições ou bloquear.
4. Definir 2 regras novas de bloqueio (mínimo).
5. Testar 1 caso que antes passava e agora deve bloquear.

### Tarefa obrigatória de experimentação
Executar ao menos 2 intervenções técnicas relevantes:
1. Prompt por papel, ou
2. Tools/permissões, ou
3. Ordem de orquestração, ou
4. Guardrail adicional, ou
5. Mudança na abordagem de embedding (utilizar modelo pronto em vez de TF-IDF, por exemplo).

Regra:
- Intervenção sem comparação baseline vs variante não vale.

## Duas intervencoes sugeridas (exemplos)
Se o grupo estiver em dúvida, usem estas duas intervenções prontas como ponto de partida.

### Intervencao A - Prompt mais rigoroso para o revisor
Objetivo:
- reduzir aprovações fracas e aumentar rastreabilidade.

Como fazer:
1. Rodem o fluxo baseline (prompt atual do revisor).
2. Alterem o prompt do revisor para exigir evidências mínimas antes de aprovar.
3. Rodem novamente e comparem a decisão final.

Exemplo de ajuste de prompt (variante):
- "Só aprove se houver pelo menos 3 evidências independentes (ticket, log e código ou teste)."
- "Se houver módulo citado que não existe, bloqueie a proposta."
- "Se o plano de testes tiver menos de 3 testes objetivos, marque aprovar com condições ou bloquear."

O que observar no A/B:
- Houve menos aprovações com evidência fraca?
- A justificativa final ficou mais concreta?
- O custo de tempo aumentou muito?

### Intervencao B - Guardrail determinístico de bloqueio
Objetivo:
- impedir que propostas avancem sem qualidade mínima.

Como fazer:
1. Definam uma regra objetiva de bloqueio.
2. Rodem baseline sem a regra.
3. Ativem a regra e rodem variante.
4. Testem um caso que passava antes para ver se agora bloqueia.

Exemplos de guardrail:
- Bloquear se confiança = alta e número de evidências < 3.
- Bloquear se não houver nenhum módulo válido do projeto na lista de afetados.
- Bloquear se não houver plano de testes com critério verificável.

O que observar no "A/B" (justificando):
- O guardrail evitou falso positivo de aprovação?
- Aumentou segurança sem travar casos bons?
- A decisão ficou mais fácil de explicar?

## Mini benchmark A/B (versão enxuta)
Façam benchmark simplificado.

Passos:
1. Definam hipítese testável.
2. Executem baseline (1 rodada).
3. Executem variante (1 rodada).
4. Comparem na tabela.

| Metrica | Baseline | Variante | Diferenca | Observacao |
|---|---:|---:|---:|---|
| Cobertura de evidencias (0-2) |  |  |  |  |
| Coerencia do diagnostico (0-2) |  |  |  |  |
| Qualidade do plano de testes (0-2) |  |  |  |  |
| Rastreabilidade da decisao (0-2) |  |  |  |  |
| Custo/tempo relativo (0-2 invertido) |  |  |  |  |

Conclusão obrigatória:
1. A variante melhorou o sistema?
2. O ganho justifica o custo?

Exemplo rapido de preenchimento (apenas referencia):

| Metrica | Baseline | Variante | Diferenca | Observacao |
|---|---:|---:|---:|---|
| Cobertura de evidencias (0-2) | 1 | 2 | +1 | Revisor passou a exigir 3 evidências independentes |
| Coerencia do diagnostico (0-2) | 1 | 2 | +1 | Menos contradições entre causa e módulos afetados |
| Qualidade do plano de testes (0-2) | 1 | 2 | +1 | Plano ficou com casos verificáveis |
| Rastreabilidade da decisao (0-2) | 1 | 2 | +1 | Decisão final cita critérios explícitos |
| Custo/tempo relativo (0-2 invertido) | 2 | 1 | -1 | Variante demorou um pouco mais |

Leitura do exemplo:
- A variante melhorou qualidade e segurana.
- O custo de tempo aumentou, mas o trade-off foi aceitável para incidentes criticos.

## O que entregar no fim da aula
Entreguem um unico arquivo markdown com este formato:

```md
# Entrega - Grupo X

## Incidente analisado
- ID:

## Diagnostico
- Causa provavel:
- Confianca (baixa/media/alta):
- Evidencias principais:

## Modulos afetados
- Lista:

## Proposta conceitual
- Descricao:
- Tipo de mudanca:
- Nao executar automaticamente: sim

## Plano de testes
1.
2.
3.

## Revisao e decisao
- Status: aprovar | aprovar com condicoes | bloquear
- Riscos/lacunas:
- Requer revisao humana: sim

## Experimento tecnico aplicado
- Tipo de intervencao:
- O que mudou:
- Por que essa mudanca foi escolhida:
- Risco que ela tenta reduzir:

## Benchmark A/B (enxuto)
- Hipotese:
- Baseline (resumo):
- Variante (resumo):
- Comparacao final:
- Decisao tecnica final:
- Trade-off principal (qualidade vs tempo ou complexidade):
```

## Rubrica de avaliacao
Cada item vale de 0 a 2 pontos. Total: 10.

1. Qualidade das evidencias.
2. Coerencia tecnica da hipotese.
3. Qualidade do plano de testes.
4. Rastreabilidade da decisao.
5. Governanca (limites de autonomia e revisao humana).

Bonus opcional (+1): benchmark muito bem justificado com trade-off claro.

## Checklist final
Antes de entregar, confiram:
1. Cada conclusao tem evidencia.
2. A proposta nao executa mudanca automatica.
3. O plano de testes e objetivo.
4. A decisao final esta justificada.
5. Existe comparacao baseline vs variante.
