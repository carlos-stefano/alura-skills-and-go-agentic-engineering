# Target Project — Incident Agent

Aplicação didática que expõe um workflow agêntico de investigação de incidentes por CLI e API local.

## Características

- LangGraph como orquestrador;
- LLM real com saída estruturada;
- recuperação local de evidências;
- validação estrutural e baseada em evidências;
- tentativas limitadas;
- política de ações;
- revisão humana simulada;
- eventos e métricas por execução;
- persistência local dos registros.

## Execução

Execute a partir da raiz do repositório para que o pacote `shared` esteja disponível:

```bash
pip install -r requirements-aula4.txt
cp target_project/incident_agent/.env.example target_project/incident_agent/.env
python -m target_project.incident_agent.app.cli investigate --incident-file target_project/incident_agent/data/incidents/incident_documented.json --knowledge-dir target_project/incident_agent/data/knowledge --env-file target_project/incident_agent/.env
```

## API

```bash
uvicorn target_project.incident_agent.app.api:app --reload
```

Abra `/docs` para visualizar a documentação interativa.

## Limite de escopo

O workflow não executa alterações reais. Ações de risco são encaminhadas para revisão humana e as demais são apenas simuladas.
