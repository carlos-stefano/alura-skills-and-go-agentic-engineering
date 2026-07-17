# Aula 3 — Engenharia de Contexto, Avaliacao e Confiabilidade

Nesta aula, voce vai evoluir de "fazer o agente funcionar" para "fazer o sistema ser confiavel".

O foco esta em tres pilares:
- engenharia de contexto para reduzir respostas vagas;
- avaliacao sistematica de qualidade;
- mecanismos de fallback e revisao humana para reduzir risco.

## O que voce vai aprender

Ao final da Aula 3, voce sera capaz de:
- montar contexto de forma controlada, sem expor dados desnecessarios;
- avaliar saidas de agentes com criterios verificaveis;
- aplicar validacao de contrato, evidencias e seguranca;
- decidir entre aceitar, tentar novamente ou escalar para revisao humana;
- executar uma regressao simples para monitorar estabilidade.

## Sequencia recomendada

1. `notebooks/01_engenharia_de_contexto_com_agentes.ipynb`
	- organiza contexto, ferramentas e limites de consulta;
	- mostra como melhorar rastreabilidade da investigacao.

2. `notebooks/02_avaliacao_de_sistemas_agenticos.ipynb`
	- define casos de avaliacao;
	- mede qualidade por propriedades (e nao por texto identico);
	- consolida resultados em relatorio.

3. `notebooks/03_fallbacks_regressao_e_revisao_humana.ipynb`
	- implementa retries com feedback verificavel;
	- limita tentativas;
	- aplica escalonamento para revisao humana quando necessario.

## Preparacao do ambiente

1. Ative seu ambiente virtual Python.
2. Instale as dependencias desta aula:

```bash
pip install -r requirements-aula3.txt
```

3. Configure as variaveis em `.env` (na raiz do repositorio ou em `Aula 3/.env`):

```text
OPENAI_API_KEY=sua_chave_aqui
MODEL_NAME=openai/gpt-4o-mini
```

## Como executar

- Abra os notebooks no VS Code ou Jupyter.
- Execute as celulas na ordem.
- Se quiser apenas validar estrutura e fluxo sem chamadas reais ao modelo, use o modo de execucao didatico presente nos notebooks quando disponivel.

## Criterios de qualidade esperados

Uma boa solucao nesta aula deve:
- citar evidencias rastreaveis do projeto;
- manter coerencia entre confianca e recomendacoes;
- evitar acoes de alto impacto sem revisao humana;
- registrar claramente o motivo de cada retry ou escalonamento.

## Problemas comuns

- `OPENAI_API_KEY` ausente: verifique o `.env` e reinicie o kernel.
- Erro de importacao de modulos compartilhados: execute a celula de setup do notebook antes das demais.
- Resultado inconsistente entre execucoes: confira temperatura do modelo e criterios de avaliacao.

## Resultado final da aula

Ao concluir a Aula 3, voce tera um fluxo agentico mais previsivel, auditavel e seguro, preparado para cenarios reais com supervisao humana.

## Rubrica de avaliacao (entregavel final)

Escala por criterio:
- 0 = nao atende;
- 1 = atende parcialmente;
- 2 = atende bem.

| Criterio | O que avaliar | Nota (0-2) |
|---|---|---|
| 1. Estrutura da saida | Contrato final completo (campos obrigatorios e tipos corretos). |  |
| 2. Rastreabilidade de evidencias | Evidencias especificas e verificaveis; sem conclusao importante sem evidencia. |  |
| 3. Coerencia da analise | Resumo, hipoteses e recomendacoes sem contradicoes logicas. |  |
| 4. Seguranca e governanca | Cautela em acoes de alto impacto; escalonamento quando necessario. |  |
| 5. Retries e fallback | Retries com feedback util e limite explicito de tentativas. |  |
| 6. Decisao final do fluxo | Decisao clara entre aceitar, tentar novamente ou revisar com humano. |  |
| 7. Regressao e estabilidade | Avaliacao por propriedades de qualidade, com comportamento estavel. |  |
| 8. Qualidade do relatorio | Resultado legivel, auditavel e com limites/incertezas explicitados. |  |

Pontuacao total: soma maxima de 16 pontos.

Interpretacao sugerida:
- 14 a 16: aprovado com seguranca;
- 11 a 13: aprovado com ressalvas;
- 8 a 10: reforco recomendado antes de concluir;
- 0 a 7: nao aprovado.

Regra de corte recomendada (gating):
- nota total minima de 12;
- obrigatorio: criterio 2 >= 1, criterio 4 >= 1 e criterio 5 >= 1.