from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Retrieval Service")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
