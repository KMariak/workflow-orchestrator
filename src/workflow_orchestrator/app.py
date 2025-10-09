from fastapi import FastAPI
from celery import Celery

from .settings import settings
from .api.main import app as api_app


# FastAPI
app = FastAPI(title="Workflow Orchestrator")
app.mount("", api_app)


# Celery
celery_app = Celery(
    "workflow_orchestrator",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
)


celery_app.autodiscover_tasks(["workflow_orchestrator.tasks"])