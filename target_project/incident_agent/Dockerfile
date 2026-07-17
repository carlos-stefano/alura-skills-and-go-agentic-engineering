FROM python:3.11-slim

WORKDIR /app

COPY requirements-aula4.txt ./requirements-aula4.txt
COPY shared ./shared
COPY target_project ./target_project

RUN pip install --no-cache-dir -r requirements-aula4.txt

EXPOSE 8000

CMD ["uvicorn", "target_project.incident_agent.app.api:app", "--host", "0.0.0.0", "--port", "8000"]
