FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install -e .

COPY src/ /app/src/

EXPOSE 8080
CMD ["uvicorn", "workflow_orchestrator.app:app", "--host", "0.0.0.0", "--port", "8080"]