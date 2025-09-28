from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ProcessStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    COMPENSATED = "compensated"


@dataclass
class StepDef:
    name: str
    forward_task: str
    compensate_task: str | None = None


@dataclass
class SagaDef:
    name: str
    steps: List[StepDef]


@dataclass
class Process:
    id: str | None
    name: str
    payload: Dict[str, Any]
    status: ProcessStatus = ProcessStatus.CREATED
    current_step: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)
    result: Dict[str, Any] | None = None