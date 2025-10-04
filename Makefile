.PHONY: install run-api fmt lint

install:
	pip install -e .

run:
	PYTHONPATH=src uv run uvicorn workflow_orchestrator.app:app --reload --port 8080

fmt:
	ruff check --fix .

lint:
	ruff check .