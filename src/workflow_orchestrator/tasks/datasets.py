import time
from ..app import celery_app

@celery_app.task(name="datasets.refresh", autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 30})
def refresh_dataset(dataset_id: str) -> dict:
    time.sleep(1)
    return {"dataset_id": dataset_id, "ok": True}

@celery_app.task(name="datasets.stats")
def compute_stats(dataset_id: str) -> dict:
    time.sleep(0.5)
    return {"dataset_id": dataset_id, "rows": 123, "cols": 17}