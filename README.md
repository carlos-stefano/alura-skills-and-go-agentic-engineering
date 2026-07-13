# Agentic Engineering - Skills and Go

Repositório principal do curso de Agentic Engineering da Alura no programa Skills & Go.

Aqui você encontra a trilha completa, do protótipo ao workflow operacional com observabilidade, API e avaliação de confiabilidade.

## Visao Geral

O curso objetiva fornecer fundamentos de desenvolvimento de sistemas agênticos, reunindo conceitos e ferramentas relevantes para desenhar sistemas inteligentes para otimização de processos. 

O curso está organizado em quatro aulas progressivas:

1. Fundamentos de workflows determinísticos, uso de LLMs (Large Language Models) e introdução a tools.
2. Investigação de incidentes com agente único e multiagentes.
3. Engenharia de contexto, avaliação sistemática e mecanismos de fallback.
4. Operacionalização com LangGraph, métricas, API local e Docker.

Cada aula possui:

- README próprio com instruções detalhadas.
- Notebooks guiados para acompanhamento prático.
- Dependências específicas via arquivo *requirements*.
- Dados de apoio para simulações e análises.

## Estrutura do Repositorio

```text
.
├── Aula 1/
├── Aula 2/
├── Aula 3/
├── Aula 4/
├── shared/
└── target_project/
```

Resumo dos diretorios principais:

- Aula 1: fundamentos de fluxo determinístico, modo demo e modo com LLM.
- Aula 2: investigação com tools reais e comparação entre arquiteturas de agentes.
- Aula 3: critérios de qualidade, contratos, revisão humana e regressão.
- Aula 4: transformação do protótipo em aplicação operacional.
- shared: módulos compartilhados entre aulas (Aula 3 e Aula 4).
- target_project: projetos-alvo usados nas práticas do curso, que podem ser referenciados em diferentes aulas.

## Projetos-alvo

O diretório **target_project** centraliza os dois projetos utilizados ao longo da trilha:

- mini_orders_pipeline: base de investigação das Aulas 2 e 3.
- incident_agent: aplicação operacional da Aula 4 (CLI, API, testes e Docker).

## Requisitos

- Python 3.10 ou superior.
- VS Code com suporte a Jupyter (recomendado) ou Jupyter Lab (ou outra IDE de sua preferência).
- Chave de API para provedores de LLM quando exigido pelas aulas. Vários `.env.example` associam uma variável da `Open AI`, mas você pode usar qualquer provedor de sua preferência.

**Observação**: as dependências são separadas por aula. Instale sempre na pasta da aula correspondente.

## Inicio Rapido

1. Clone o repositório.
2. Escolha a aula que deseja executar.
3. Crie e ative um ambiente virtual Python.
4. Instale as dependências da aula.
5. Configure as variáveis de ambiente (quando necessário).
6. Execute os notebooks na ordem sugerida no README da aula.

Exemplo genérico de setup:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

## Trilha Recomendada

1. Aula 1: consolidar os conceitos básicos e o ciclo de decisão de agentes.
2. Aula 2: aplicar tools em investigação com evidências reais, explorando especialmente a distribuição de papeis para múltiplos agentes.
3. Aula 3: elevar confiabilidade com avaliação e governança.
4. Aula 4: empacotar e operar o workflow em formato de aplicação.

## Como Navegar no Conteudo

- Comece sempre pelo README da aula antes de abrir os notebooks.
- Use os notebooks na sequência sugerida para manter o contexto didatico.
- Consulte *shared* quando quiser entender componentes reutilizados entre aulas.
- Consulte *target_project* para estudar os cenarios reais usados nos exercicios.

## Boas Praticas Durante o Curso

- Trabalhe com ambientes virtuais isolados por aula.
- Mantenha as variáveis de ambiente fora do controle de versão.
- Execute as células de setup dos notebooks antes das demais.
- Registre evideências e justificativas nas etapas de investigação e proposta.

## Solucao de Problemas Comuns

- Erros de importação: verifique se o notebook executou a celula de setup de caminho.
- Variáveis de ambiente não reconhecidas: confirme o arquivo .env e reinicie o kernel.
- Diferença de resultados entre execuções: revise modelo, temperatura e critérios da aula.
