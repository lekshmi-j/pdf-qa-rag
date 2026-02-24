from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import json

from app.core.prompt_builder import build_prompt
from app.core.llm_client import stream_answer

router = APIRouter()

RETRIEVAL_URL = "http://127.0.0.1:8001/retrieve"


class AnswerRequest(BaseModel):
    question: str
    top_k: int = 2


@router.post("/answer")
def answer_question(request: AnswerRequest):

    print("Answer endpoint called with question:", request.question)
    try:
        retrieval_response = requests.post(
            RETRIEVAL_URL,
            json={
                "query": request.question,
                "top_k": request.top_k
            },
            timeout=None
        )
        print("Retrieval response status:", retrieval_response.status_code)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Retrieval service unreachable: {str(e)}")

    if retrieval_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Retrieval service failed.")

    retrieval_data = retrieval_response.json()
    contexts = retrieval_data.get("contexts", [])

    if not contexts:
        def empty_stream():
            yield json.dumps({
                "type": "token",
                "content": "I don't know based on the provided documents."
            }) + "\n"
            yield json.dumps({"type": "done"}) + "\n"

        return StreamingResponse(empty_stream(), media_type="application/json")

    prompt = build_prompt(request.question, contexts)

    # Precompute sources
    sources = sorted({
        f"{ctx['metadata']['source']} (page {ctx['metadata']['page']})"
        for ctx in contexts
    })

    def token_generator():
        try:
            # Stream tokens
            for token in stream_answer(prompt):
                yield json.dumps({
                    "type": "token",
                    "content": token
                }) + "\n"

            # After streaming tokens, send sources
            yield json.dumps({
                "type": "sources",
                "content": sources
            }) + "\n"

            yield json.dumps({"type": "done"}) + "\n"

        except Exception as e:
            yield json.dumps({
                "type": "error",
                "content": str(e)
            }) + "\n"

    return StreamingResponse(token_generator(), media_type="application/json")