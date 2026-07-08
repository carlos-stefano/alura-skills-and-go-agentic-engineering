# Agentic Engineering — Aula 1

Este repositório contém o material da Aula 1 de Agentic Engineering, contemplando tópicos como:
- conceitos de agentes e ferramentas (tool-calling);
- exemplos práticos com notebook e código Python;
- modo demo determinístico e modo com LLM real.

## O que está neste repositório

- `notebooks/Aula 1A - Introdução a workflows determinísticos e LLMs.ipynb`
  - workflow linear de incidentes com OpenAI Responses e parse estruturado;
  - demonstra uso de Pydantic para validação de saída;
  - compara utilização de LLMs com parser, ou não, de saída.

- `notebooks/Aula_1_Agentes_Tools.ipynb`
  - complemento sobre agentes que chamam ferramentas;
  - modo demonstração sem API para visualizar o ciclo de decisão, execução e resposta.

- `data/`
  - bases de exemplos usadas nos notebooks (tickets, runbooks, logs, status de serviço).

## Preparação do ambiente

1. Crie e ative um ambiente Python isolado.

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo de exemplo de variáveis de ambiente:

```bash
copy .env.example .env
```

4. Configure as variáveis no `.env`:

```text
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=nome_do_modelo
USE_DEMO_MODE=true
```

- `USE_DEMO_MODE=true`: roda apenas a parte didática sem chamar o modelo.
- `USE_DEMO_MODE=false`: ativa o modo LLM real, usando `OPENAI_API_KEY` e `OPENAI_MODEL`.

## Como usar

Abra os notebooks no Jupyter ou no VS Code e execute as células na ordem apresentada.

Recomendações:
- execute primeiro `Aula_1_Fluxos_Agentic_Guia.ipynb` para entender o fluxo básico;
- depois abra `Aula_1_Agentes_Tools.ipynb` para ver a versão com ferramentas e agente.

## Problemas comuns

- Se o notebook não encontrar a chave, verifique se o kernel está usando o mesmo diretório onde está o `.env`.
- Reinicie o kernel sempre que modificar o `.env`.
- O nome da variável é `OPENAI_API_KEY`; `OPEN_API_KEY` está incorreto.

## Observações para alunos

- O modo demo é útil para aprender o padrão sem custo ou dependência de API.
- A célula opcional de LangChain só deve ser executada se você tiver um modelo compatível e as bibliotecas instaladas.
- O foco da aula é entender arquitetura e fluxo, não apenas gerar texto com o modelo.
