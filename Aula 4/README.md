# Aula 4 — Operacionalização de Sistemas Multiagentes com LangGraph

Este diretório contém a proposta completa da Aula 4 da formação **Agentic Engineering**.

A aula parte de um protótipo funcional e trabalha sua transformação em uma aplicação multiagente organizada, rastreável e preparada para evolução. A arquitetura multiagente é utilizada como objeto de estudo, não como recomendação universal: o material inclui um baseline de agente único para comparação de qualidade, custo, latência e complexidade.

## Agentes do workflow

O LangGraph coordena quatro chamadas reais a LLMs:

1. **agente de triagem** — classifica o incidente e escolhe ferramentas e consultas;
2. **agente investigador** — formula hipóteses usando somente as evidências recuperadas;
3. **agente revisor** — avalia alinhamento com evidências e decide aprovar, revisar ou escalar;
4. **agente planejador de ação** — propõe uma ação estruturada, sem executá-la.

Os componentes determinísticos permanecem responsáveis por:

- execução controlada das ferramentas selecionadas;
- validação estrutural e de referências às evidências;
- limites de retry;
- aplicação da política de ações;
- bloqueio e escalonamento humano;
- métricas, eventos e persistência.

```text
triage_agent
     ↓
execute_tools
     ↓
investigation_agent
     ↓
deterministic_validation
     ↓
review_agent
  ↙      ↘
retry   action_planner_agent
            ↓
       policy_check
         ↙     ↘
 human_review  simulation
```

## Objetivos da aula

Ao final, os alunos deverão ser capazes de:

- representar estado, nós e rotas condicionais com LangGraph;
- distinguir chamada de agente, execução de ferramenta e controle determinístico;
- construir um workflow com agentes especializados e contratos explícitos;
- aplicar revisão, tentativas limitadas e intervenção humana;
- registrar eventos, latência, tokens, custo e falhas por agente;
- disponibilizar o mesmo workflow por CLI e API local;
- empacotar a aplicação com Docker;
- avaliar quando uma solução multiagente se justifica e quando um agente único é suficiente.

## Estrutura

```text
.
├── notebooks/
│   ├── 01_do_prototipo_ao_workflow_operacional.ipynb
│   ├── 02_observabilidade_e_metricas.ipynb
│   ├── 03_autonomia_controlada_api_e_docker.ipynb
│   └── GUIA_DOCENTE.md
└── requirements-aula4.txt
```

Recursos compartilhados desta aula ficam fora desta pasta:

- `shared/aula_4` concentra o código compartilhado da Aula 4;
- `target_project/incident_agent` contém a aplicação operacional usada nos notebooks.

## Observação sobre `shared`

`shared/aula_4` contém somente as adições propostas para esta aula, facilitando a mesclagem com o diretório `shared` já existente no curso. As funções de domínio não dependem do LangGraph; apenas a montagem e o roteamento do grafo conhecem o framework.

## Programação funcional

O projeto evita classes de serviço. Estado e resultados são dicionários explícitos; comportamento é expresso por funções. `TypedDict` é usado apenas como contrato estático das estruturas de dados e das saídas estruturadas dos modelos.

## Execução rápida

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-aula4.txt
cp target_project/incident_agent/.env.example target_project/incident_agent/.env
python -m target_project.incident_agent.app.cli investigate \
     --incident-file target_project/incident_agent/data/incidents/incident_documented.json \
     --knowledge-dir target_project/incident_agent/data/knowledge \
     --env-file target_project/incident_agent/.env
```

Para iniciar a API:

```bash
uvicorn target_project.incident_agent.app.api:app --reload
```

A aplicação exige `OPENAI_API_KEY`, ou adaptação do provedor em `shared/aula_4/llm.py`.

## Comparação arquitetural

O arquivo `target_project/incident_agent/app/single_agent_baseline.py` oferece uma alternativa compacta. Ele não pretende ser uma solução completa, mas apoiar a discussão:

- a especialização melhorou o resultado?
- o revisor encontrou problemas relevantes?
- o custo e a latência adicionais são aceitáveis?
- o fluxo ficou mais fácil ou mais difícil de manter?

## Docker

A imagem deve ser construída a partir da raiz, porque utiliza `shared` e `target_project`:

```bash
docker build -f target_project/incident_agent/Dockerfile -t incident-agent-aula4 .
docker run --env-file target_project/incident_agent/.env -p 8000:8000 incident-agent-aula4
```
