# Aula 3 — Engenharia de Contexto, Avaliação e Confiabilidade

Nesta aula, você vai evoluir de "fazer o agente funcionar" para "fazer o sistema ser confiável".

O foco está em três pilares:
- engenharia de contexto para reduzir respostas vagas;
- avaliação sistemática de qualidade;
- mecanismos de fallback e revisão humana para reduzir risco.

## O que você vai aprender

Ao final da Aula 3, voce será capaz de:
- montar contexto de forma controlada, sem expor dados desnecessários;
- avaliar saídas de agentes com critérios verificáveis;
- aplicar validacao de contrato, evidências e segurança;
- decidir entre aceitar, tentar novamente ou escalar para revisão humana;
- executar uma regressão simples para monitorar estabilidade.

## Sequência recomendada

1. `notebooks/3A Engenharia de contexto com agentes.ipynb`
	- organiza contexto, ferramentas e limites de consulta;
	- mostra como melhorar rastreabilidade da investigação.

2. `notebooks/3B Avaliação de sistemas agênticos.ipynb`
	- define casos de avaliação;
	- mede qualidade por propriedades (e nao por texto idêntico);
	- consolida resultados em relatório.

3. `notebooks/3C Fallbacks, regressão e revisão humana.ipynb`
	- implementa retries com feedback verificável;
	- limita tentativas;
	- aplica escalonamento para revisão humana quando necessário.

## Preparação do ambiente

1. Ative seu ambiente virtual Python.
2. Instale as dependências desta aula:

```bash
pip install -r requirements-aula3.txt
```

3. Configure as variáveis em `.env` (na raiz do repositorio ou em `Aula 3/.env`):

```text
OPENAI_API_KEY=sua_chave_aqui
MODEL_NAME=openai/gpt-4o-mini
```

## Como executar

- Abra os notebooks no VS Code ou Jupyter.
- Execute as celulas na ordem.
- Se quiser apenas validar estrutura e fluxo sem chamadas reais ao modelo, use o modo de execução didático presente nos notebooks quando disponível.

## Critérios de qualidade esperados

Uma boa solução nesta aula deve:
- citar evidências rastreáveis do projeto;
- manter coerência entre confiança e recomendações;
- evitar ações de alto impacto sem revisão humana;
- registrar claramente o motivo de cada retry ou escalonamento.

## Problemas comuns

- `OPENAI_API_KEY` ausente: verifique o `.env` e reinicie o kernel.
- Erro de importação de módulos compartilhados: execute a célula de setup do notebook antes das demais.
- Resultado inconsistente entre execuções: confira temperatura do modelo e critérios de avaliação.

## Resultado final da aula

Ao concluir a Aula 3, voce terá um fluxo agentico mais previsível, auditável e seguro, preparado para cenários reais com supervisão humana.

## Rubrica de avaliacao (entregável final)

Escala por critério:
- 0 = não atende;
- 1 = atende parcialmente;
- 2 = atende bem.

| Critério | O que avaliar | Nota (0-2) |
|---|---|---|
| 1. Estrutura da saóda | Contrato final completo (campos obrigatórios e tipos corretos). |  |
| 2. Rastreabilidade de evidências | Evidências específicas e verificáveis; sem conclusão importante sem evidência. |  |
| 3. Coerência da análise | Resumo, hipóteses e recomendacões sem contradições lógicas. |  |
| 4. Segurança e governança | Cautela em ações de alto impacto; escalonamento quando necessário. |  |
| 5. Retries e fallback | Retries com feedback útil e limite explícito de tentativas. |  |
| 6. Decisão final do fluxo | Decisão clara entre aceitar, tentar novamente ou revisar com humano. |  |
| 7. Regressão e estabilidade | Avaliacão por propriedades de qualidade, com comportamento estável. |  |
| 8. Qualidade do relatório | Resultado legível, auditável e com limites/incertezas explicitados. |  |

Pontuação total: soma máxima de 16 pontos.

Interpretação sugerida:
- 14 a 16: aprovado com segurança;
- 11 a 13: aprovado com ressalvas;
- 8 a 10: reforço recomendado antes de concluir;
- 0 a 7: não aprovado.

Regra de corte recomendada (gating):
- nota total mínima de 12;
- obrigatório: critério 2 >= 1, critério 4 >= 1 e critério 5 >= 1.