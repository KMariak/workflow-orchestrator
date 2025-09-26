.PHONY: install run-api fmt lint

install:
\tpip install -e .

run-api:
\tuvicorn workflow_orchestrator.app:app --reload --port 8080

fmt:
\truff check --fix .

lint:
\truff check .