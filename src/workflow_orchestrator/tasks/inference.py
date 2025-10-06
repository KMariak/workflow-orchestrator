from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from ..app import celery_app



class TransientError(RuntimeError):
    """Temporary infra/network error, safe to retry."""



@celery_app.task(name="inference.warmup", ignore_result=True)
def warmup(model_name: str = "baseline") -> None:
    # TODO: lazily load model into a module/global cache
    time.sleep(0.2)  # demo delay


@celery_app.task(
    name="inference.predict",
    bind=True,
    autoretry_for=(TransientError,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def predict(
    self,
    input_data: Dict[str, Any],
    model_name: str = "baseline",
    callback_url: Optional[str] = None,  # якщо використовуєш callback-патерн
) -> Dict[str, Any]:
    # TODO: validate input_data (schema), run model
    try:
        score = float(hash(str(input_data)) % 100) / 100.0
        result = {
            "ok": True,
            "model": model_name,
            "prediction": {"score": score, "label": "positive" if score > 0.5 else "negative"},
            "meta": {"task_id": self.request.id},
        }
    except TimeoutError as e:
        raise TransientError(str(e)) from e
    except Exception as e:
        result = {"ok": False, "error": str(e), "meta": {"task_id": self.request.id}}
        return result

    if callback_url:
        try:
            import requests  # lightweight sync; для high-load краще async/queue
            requests.post(callback_url, json={"task": "inference.predict", "result": result}, timeout=3)
        except Exception:
            pass

    return result


@celery_app.task(
    name="inference.batch_predict",
    bind=True,
    autoretry_for=(TransientError,),
    retry_backoff=2,             # backoff із множником
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def batch_predict(
    self,
    items: List[Dict[str, Any]],
    model_name: str = "baseline",
    limit: int = 1000,
) -> Dict[str, Any]:
    if len(items) > limit:
        return {"ok": False, "error": f"batch too large (> {limit})", "meta": {"task_id": self.request.id}}

    outputs = []
    for it in items:
        score = float(hash(str(it)) % 100) / 100.0
        outputs.append({"input": it, "score": score})

    return {
        "ok": True,
        "model": model_name,
        "count": len(outputs),
        "predictions": outputs,
        "meta": {"task_id": self.request.id},
    }