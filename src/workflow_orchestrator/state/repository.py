from __future__ import annotations
from typing import Dict, Optional
from uuid import uuid4
from .models import Process
from ..orchestration.ports.process_repo_port import ProcessRepoPort

class InMemoryProcessRepo(ProcessRepoPort):
    def __init__(self) -> None:
        self._db: Dict[str, Process] = {}

    async def create(self, process: Process) -> str:
        pid = process.id or str(uuid4())
        process.id = pid
        self._db[pid] = process
        return pid

    async def load(self, pid: str) -> Optional[Process]:
        return self._db.get(pid)

    async def save(self, process: Process) -> None:
        if not process.id:
            raise ValueError("Process must have id before save()")
        self._db[process.id] = process