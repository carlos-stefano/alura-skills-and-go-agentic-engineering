# Agentic Engineering - Aula 1

Este material foi organizado para estudo pratico, com foco em construir um workflow de triagem de incidentes combinando:
- etapas deterministicas;
- uso de LLM com saida estruturada;
- ferramentas controladas e validacoes de dominio.

## Objetivos de aprendizagem

Ao final da Aula 1, voce deve conseguir:
1. Diferenciar responsabilidades entre modelo e codigo deterministico.
2. Definir contratos de saida estruturada para interpretacao e sintese.
3. Aplicar validacoes de negocio alem da validacao de formato.
4. Explicar quando usar workflow linear e quando usar tool calling.

## Entregaveis esperados

1. Interpretacao estruturada de ticket validada.
2. Analise inicial com evidencias, hipoteses e proximos passos.
3. Rastreio do fluxo com etapas explicitas de decisao e validacao.

## Estrutura da Aula 1

- `notebooks/Aula 1A - Introdução a workflows determinísticos e LLMs.ipynb`
  - fluxo linear de triagem com contrato estruturado;
  - comparacao entre saida livre e parse estruturado;
  - validacoes deterministicas e workflow ponta a ponta.

- `notebooks/Aula 1B - Agentes e tools.ipynb`
  - transicao do fluxo linear para agente com ferramenta;
  - visualizacao do ciclo decisao -> tool call -> resposta;
  - versao opcional com agente real e representacao no Langflow.

- `data/`
  - bases usadas nas praticas (tickets, logs, status e runbooks).

## Trilha recomendada

1. Execute primeiro o notebook 1A.
2. Conclua os checkpoints de cada secao.
3. Execute o notebook 1B e compare os dois desenhos arquiteturais.

Tempo sugerido:
- 1A: 60 a 90 min
- 1B: 45 a 75 min

## Preparacao do ambiente

1. Crie e ative um ambiente Python isolado.
2. Instale dependencias:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo de exemplo de variaveis:

```bash
copy .env.example .env
```

4. Configure o `.env`:

```text
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=nome_do_modelo
USE_DEMO_MODE=true
```

Modos de execucao:
- `USE_DEMO_MODE=true`: executa sem chamadas reais ao modelo.
- `USE_DEMO_MODE=false`: ativa chamadas reais com `OPENAI_API_KEY` e `OPENAI_MODEL`.

## Criterios de sucesso

Ao finalizar os dois notebooks, confirme:
1. Voce consegue explicar o papel de contrato estruturado no fluxo.
2. Voce identifica onde entram validacoes deterministicas.
3. Voce diferencia claramente consulta automatica do workflow linear e consulta decidida por agente.
4. Voce justifica decisoes de escalonamento com evidencias observaveis.

## Problemas comuns

- Chave nao encontrada: confirme se o kernel esta no mesmo diretorio do `.env`.
- Mudanca no `.env`: reinicie o kernel apos alterar variaveis.
- Variavel incorreta: use `OPENAI_API_KEY` (nao `OPEN_API_KEY`).

## Dicas de estudo

- Priorize entender o fluxo e as garantias de seguranca antes de otimizar prompts.
- Compare sempre saida demo e saida com LLM para analisar variabilidade.
- Se algo falhar, volte ao checkpoint da secao antes de seguir.
