#!/usr/bin/env bash
set -e

echo ">>> Creating project structure for workflow-orchestrator..."

# 1. Root

# 2. Base files
touch pyproject.toml README.md .env.example Dockerfile docker-compose.yml Makefile
mkdir -p .circleci
touch .circleci/config.yml

# 3. Src root
mkdir -p src/workflow_orchestrator

# Core
touch src/workflow_orchestrator/__init__.py
touch src/workflow_orchestrator/settings.py
touch src/workflow_orchestrator/logging.py
touch src/workflow_orchestrator/app.py
touch src/workflow_orchestrator/routing.py
touch src/workflow_orchestrator/observability.py

# API
mkdir -p src/workflow_orchestrator/api
touch src/workflow_orchestrator/api/__init__.py
touch src/workflow_orchestrator/api/main.py
touch src/workflow_orchestrator/api/schemas.py

# Tasks
mkdir -p src/workflow_orchestrator/tasks
touch src/workflow_orchestrator/tasks/__init__.py
touch src/workflow_orchestrator/tasks/datasets.py
touch src/workflow_orchestrator/tasks/training.py
touch src/workflow_orchestrator/tasks/inference.py

# Orchestration
mkdir -p src/workflow_orchestrator/orchestration
touch src/workflow_orchestrator/orchestration/__init__.py
touch src/workflow_orchestrator/orchestration/saga.py
touch src/workflow_orchestrator/orchestration/engine.py
touch src/workflow_orchestrator/orchestration/registry.py

# State
mkdir -p src/workflow_orchestrator/state
touch src/workflow_orchestrator/state/__init__.py
touch src/workflow_orchestrator/state/models.py
touch src/workflow_orchestrator/state/repository.py
touch src/workflow_orchestrator/state/locks.py

echo ">>> Project structure created successfully."
