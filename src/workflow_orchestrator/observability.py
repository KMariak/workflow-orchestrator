from fastapi import APIRouter
import time
import psutil
import platform

router = APIRouter(tags=["observability"])


@router.get("/health", summary="Basic health check")
async def health() -> dict:
    """Simple readiness check for orchestrator API."""
    return {"status": "ok"}


@router.get("/system", summary="System metrics (demo)")
async def system_metrics() -> dict:
    """
    Minimal system info for local debugging.
    In production you'd expose Prometheus metrics here.
    """
    return {
        "hostname": platform.node(),
        "platform": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }