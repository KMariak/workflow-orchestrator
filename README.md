# Workflow Orchestrator

A service for orchestrating workflows and tasks (based on Celery + FastAPI).  
Provides a thin REST API for starting processes, tracking status, and handling orchestration logic.

---

## Project Structure

workflow-orchestrator/
├─ pyproject.toml
├─ README.md
├─ .env.example
├─ Dockerfile
├─ docker-compose.yml
├─ Makefile
├─ .circleci/
│  └─ config.yml
└─ src/
└─ workflow_orchestrator/
├─ init.py
├─ settings.py             # configuration via Pydantic
├─ logging.py              # structured logging
├─ app.py                  # Celery app factory
├─ routing.py              # queues & routes
├─ observability.py        # metrics/tracing hooks
├─ api/
│  ├─ init.py
│  ├─ main.py              # FastAPI app
│  └─ schemas.py           # API schemas
├─ tasks/
│  ├─ init.py
│  ├─ datasets.py          # dataset-related tasks
│  ├─ training.py          # training tasks
│  └─ inference.py         # inference tasks
├─ orchestration/
│  ├─ init.py
│  ├─ saga.py              # saga definitions (steps/compensations)
│  ├─ engine.py            # orchestration logic
│  └─ registry.py          # process registry
└─ state/
├─ init.py
├─ models.py            # process/state models
├─ repository.py        # Mongo repository
└─ locks.py             # Redis locks & idempotency

---

## Getting Started

```bash
# install dependencies
pip install -e .

# run API
uvicorn workflow_orchestrator.api.main:app --reload --port 8080

# run Celery worker
celery -A workflow_orchestrator.app.celery_app worker -l info

# run Celery beat (optional for scheduled jobs)
celery -A workflow_orchestrator.app.celery_app beat -l info

