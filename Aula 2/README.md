# Aula 2 — Agentes com tools e investigação de incidentes

Nesta aula, você vai evoluir dos exemplos da Aula 1 para cenários mais próximos de produção: agentes que decidem quando usar ferramentas, consultam evidências reais e analisam um projeto-alvo.

## O que você vai praticar

- Investigar incidentes técnicos a partir de tickets, logs, runbooks e políticas.
- Fazer agentes consultarem arquivos do projeto e resultados de testes.
- Comparar abordagens com agente único e multiagentes.
- Produzir uma proposta de correção com justificativas e riscos.

Regra central da aula:

> As evidências não são pré-processadas para o modelo. Os agentes recebem tools e escolhem quando e como usá-las durante a investigação.

## Estrutura da pasta

```text
Aula 2/
├── notebooks/
│   ├── Aula 2A - Agente único para resolução.ipynb
│   ├── Aula 2B - Passando para Multiagentes.ipynb
│   ├── Aula 2C - Multiagentes com Langgraph.ipynb
│   └── Aula 2D - Revisão, limites e evoluções.ipynb
├── data/
│   ├── tickets/
│   ├── logs/
│   ├── runbooks/
│   ├── historico/
│   └── policies/
├── target_project/
│   ├── src/mini_orders_pipeline/
│   ├── tests/
│   └── data_samples/
├── outputs/
└── README.md
```

## Trilha recomendada

### Aula 2A - Agente único para resolução

Comece com um agente único que usa tools para levantar contexto, ler evidências e propor um caminho de correção.

### Aula 2B - Passando para Multiagentes

Quebre o problema em papéis especializados e compare com a abordagem de agente único.

### Aula 2C - Multiagentes com Langgraph

Orquestre o fluxo com estados e transições explícitas para tornar o processo mais previsível.

### Aula 2D - Revisão, limites e evoluções

Valide saídas, discuta fronteiras de automação e consolide critérios de qualidade para propostas técnicas.

## Como executar

Na pasta `Aula 2`, crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Depois, crie o arquivo `.env`:

```text
OPENAI_API_KEY=sua_chave_aqui
```

Os notebooks usam LLMs reais. Sem a variável `OPENAI_API_KEY`, as células agênticas não executam.

## Resultado esperado

Ao final da aula, você terá:

- Uma análise estruturada do incidente.
- Mapeamento dos módulos potencialmente afetados no projeto-alvo.
- Uma proposta técnica de correção com racional e limites explícitos.

Observação: nesta etapa, o foco é investigação e proposta. A geração automática de patch e PR fica para etapas posteriores do curso.
