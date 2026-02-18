from fastapi import APIRouter
from pydantic import BaseModel
from app.core.retriever import retrieve

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    score_threshold: float | None = None
    source: str | None = None

@router.post("/retrieve")
def retrieve_context(request: QueryRequest):
    results = retrieve(
        query=request.query,
        top_k=request.top_k,
        score_threshold=request.score_threshold,
        source_filter=request.source
    )

    return {
        "query": request.query,
        "contexts": results
    }
