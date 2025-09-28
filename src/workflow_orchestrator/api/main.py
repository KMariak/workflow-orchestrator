from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from .schemas import StartProcessRequest, ProcessResponse
from ..state.models import Process, ProcessStatus  # тимчасово тримаємо домен тут

app = FastAPI(title="Workflow Orchestrator API (Stage 1)")

# Тимчасове in-memory "сховище" тільки для Етапу 1
_DB: Dict[str, Process] = {}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/processes/{name}", response_model=ProcessResponse)
async def start_process(name: str, req: StartProcessRequest):
    pid = str(uuid4())
    proc = Process(
        id=pid,
        name=name,
        payload=req.payload or {},
        status=ProcessStatus.CREATED,
        current_step=0,
        history=[],
        result=None,
    )
    _DB[pid] = proc

    return ProcessResponse(
        id=pid,
        name=name,
        status=proc.status.value,
        result=proc.result,
        history=proc.history,
    )


@app.get("/processes/{pid}", response_model=ProcessResponse)
async def get_status(pid: str):
    proc = _DB.get(pid)
    if not proc:
        raise HTTPException(status_code=404, detail="Process not found")

    return ProcessResponse(
        id=proc.id,
        name=proc.name,
        status=proc.status.value,
        result=proc.result,
        history=proc.history,
    )