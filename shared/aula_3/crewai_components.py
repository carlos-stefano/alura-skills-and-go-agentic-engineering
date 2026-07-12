import json
import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool

from .project_access import (
    list_project_files,
    read_project_file,
    search_project,
    to_json,
)


def build_llm(model_name=None, temperature=0):
    return LLM(
        model=model_name or os.getenv("MODEL_NAME", "openai/gpt-4o-mini"),
        temperature=temperature,
    )


def build_project_tools(project_root, catalog, event_log=None):
    events = event_log if event_log is not None else []

    def register(tool_name, tool_input, tool_output):
        events.append({
            "tool_name": tool_name,
            "tool_input": tool_input,
            "tool_output_preview": str(tool_output)[:1000],
        })
        return tool_output

    @tool("list_target_project_files")
    def list_target_project_files() -> str:
        """Lista arquivos textuais permitidos dentro do target_project."""
        output = list_project_files(project_root)
        return to_json(register("list_target_project_files", {}, output))

    @tool("search_target_project")
    def search_target_project(query: str, top_k: int = 5) -> str:
        """Busca evidências relevantes no target_project usando consulta textual."""
        output = search_project(query=query, catalog=catalog, top_k=top_k)
        return to_json(register(
            "search_target_project",
            {"query": query, "top_k": top_k},
            output,
        ))

    @tool("read_target_project_file")
    def read_target_project_file(relative_path: str) -> str:
        """Lê um arquivo permitido do target_project pelo caminho relativo."""
        output = read_project_file(project_root, relative_path)
        return to_json(register(
            "read_target_project_file",
            {"relative_path": relative_path},
            output,
        ))

    return {
        "tools": [
            list_target_project_files,
            search_target_project,
            read_target_project_file,
        ],
        "events": events,
    }


def build_investigation_crew(
    incident,
    tools,
    llm,
    context_policy,
    reviewer=True,
    verbose=True,
):
    investigator = Agent(
        role="Investigador técnico de incidentes",
        goal=(
            "Investigar o incidente usando ferramentas, formular hipóteses "
            "e citar somente evidências realmente consultadas."
        ),
        backstory=(
            "Você é criterioso, não supõe que uma informação exista e prefere "
            "declarar incerteza quando as evidências são insuficientes."
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=verbose,
        max_iter=8,
    )

    review_agent = Agent(
        role="Revisor de confiabilidade",
        goal=(
            "Revisar criticamente a investigação, eliminar conclusões não sustentadas "
            "e devolver uma análise estruturada."
        ),
        backstory=(
            "Você atua como uma segunda linha de defesa. Uma resposta bem escrita "
            "não é suficiente: toda conclusão precisa ser rastreável."
        ),
        tools=tools,
        llm=llm,
        allow_delegation=False,
        verbose=verbose,
        max_iter=6,
    )

    investigation_task = Task(
        description=f"""
Investigue o incidente abaixo.

INCIDENTE:
{json.dumps(incident, ensure_ascii=False, indent=2)}

POLÍTICA DE CONTEXTO:
{context_policy}

Você decide quais ferramentas utilizar. Não receba o conteúdo integral do projeto
antecipadamente. Busque e leia somente os arquivos necessários.

Requisitos:
- cite identificadores no formato project:caminho/arquivo;
- diferencie fatos, hipóteses e lacunas;
- não invente evidências;
- não recomende ações destrutivas ou de produção sem revisão humana.
""",
        expected_output=(
            "Relatório técnico com classificação, resumo, hipóteses, evidências "
            "consultadas, confiança e necessidade de revisão humana."
        ),
        agent=investigator,
    )

    tasks = [investigation_task]

    if reviewer:
        review_task = Task(
            description="""
Revise a investigação anterior.

Verifique:
1. se as evidências citadas foram realmente consultadas;
2. se as hipóteses são proporcionais às evidências;
3. se a confiança é coerente;
4. se riscos ou falta de informação exigem revisão humana.

Responda SOMENTE com JSON válido, sem markdown, obedecendo exatamente:
{
  "incident_id": "string",
  "classification": "string",
  "summary": "string",
  "hypotheses": ["string"],
  "evidence_ids": ["project:caminho"],
  "recommended_actions": ["string"],
  "confidence": 0.0,
  "requires_human_review": true
}
""",
            expected_output="Um único objeto JSON válido no contrato solicitado.",
            agent=review_agent,
            context=[investigation_task],
        )
        tasks.append(review_task)

    return Crew(
        agents=[investigator, review_agent] if reviewer else [investigator],
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
    )


def parse_crew_json(result):
    raw = getattr(result, "raw", str(result)).strip()
    cleaned = raw

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()

    return json.loads(cleaned)
