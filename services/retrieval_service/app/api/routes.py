from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from app.core.retriever import retrieve

router = APIRouter()

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the refund policy?")
    top_k: int = Field(default=5, example=5)
    score_threshold: Optional[float] = Field(
        default=2,
        example=None,
        description="Optional La2 distance threshold (lower = stricter)"
    )
    source: Optional[str] = Field(
        default="",
        example=None,
        description="Optional PDF filename filter"
    )

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
