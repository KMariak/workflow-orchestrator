# Workflow Orchestrator

A service for orchestrating workflows and tasks (based on Celery + FastAPI).  
Provides a thin REST API for starting processes, tracking status, and handling orchestration logic.

---

## Project Structure

```bash
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

Got it — let’s simplify and rewrite your README in clear English.

⸻

Workflow Orchestrator

A service for orchestrating workflows and tasks.
Built with FastAPI (API) and Celery (task engine).
Dependencies managed with uv.

⸻

Getting Started
1. Install dependencies
uv venv
uv sync
source .venv/bin/activate

2. Run the API
uv run uvicorn --app-dir src workflow_orchestrator.api.main:app --reload --port 8080

Docs: http://127.0.0.1:8080/docs

3. Run a Celery worker

uv run celery -A workflow_orchestrator.app.celery_app worker -l info -Q default,io,long

4. Run Celery beat (optional)

uv run celery -A workflow_orchestrator.app.celery_app beat -l info

