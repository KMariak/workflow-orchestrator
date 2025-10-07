from dataclasses import dataclass
from typing import Optional

@dataclass
class SagaStep:
    name: str
    forward_task: str
    compensate_task: Optional[str] = None