from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class StartProcessRequest(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)


class ProcessResponse(BaseModel):
    id: str
    name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    history: Optional[list[dict]] = None