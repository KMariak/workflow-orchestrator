from ..state.models import SagaDef, StepDef

_REG: dict[str, SagaDef] = {}

def register(saga: SagaDef) -> None:
    _REG[saga.name] = saga

def get_saga(name: str) -> SagaDef | None:
    return _REG.get(name)


register(SagaDef(
    name="datasets-refresh",
    steps=[
        StepDef(name="refresh", forward_task="datasets.refresh"),
        StepDef(name="stats",   forward_task="datasets.stats"),
    ]
))