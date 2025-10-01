from typing import Optional
from ..state.models import Process, ProcessStatus
from .ports.process_repo_port import ProcessRepoPort
from .ports.task_bus_port import TaskBusPort
from . import registry

class ProcessService:
    def __init__(self, repo: ProcessRepoPort, bus: TaskBusPort) -> None:
        self.repo = repo
        self.bus = bus

    async def start(self, name: str, payload: dict) -> str:
        saga = registry.get_saga(name)
        if not saga:
            raise ValueError(f"Unknown process '{name}'")

        process = Process(
            id=None, name=name, payload=payload or {},
            status=ProcessStatus.RUNNING, current_step=0, history=[], result=None
        )
        pid = await self.repo.create(process)

        # enqueue перший крок
        first = saga.steps[0]
        task_id = self.bus.enqueue(first.forward_task, payload or {})
        process.history.append({"step": first.name, "task_id": task_id, "state": "PENDING"})
        await self.repo.save(process)
        return pid

    async def status(self, pid: str) -> Optional[Process]:
        return await self.repo.load(pid)