"""
Entry-point API для Етапу 0/1.
Run: uvicorn workflow_orchestrator.app:app --reload --port 8080
"""
from .api.main import app