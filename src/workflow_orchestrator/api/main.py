from fastapi import FastAPI

app = FastAPI(title="Workflow Orchestrator API")

@app.get("/health")
async def health():
    return {"status": "ok"}