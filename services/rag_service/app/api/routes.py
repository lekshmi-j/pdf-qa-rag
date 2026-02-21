from fastapi import APIRouter
from pydantic import BaseModel
from app.core.prompt_builder import build_prompt
from app.core.llm_client import generate_answer
import requests

router = APIRouter()

RETRIEVAL_URL = "http://127.0.0.1:8001/retrieve"


class AnswerRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("/answer")
def answer_question(request: AnswerRequest):
    print("retrieval calling")

    # 🔹 Step 1: Call Retrieval Service
    retrieval_response = requests.post(
        RETRIEVAL_URL,
        json={
            "query": request.question,
            "top_k": request.top_k
        }
    )

    if retrieval_response.status_code != 200:
        return {"error": "Retrieval service failed."}

    retrieval_data = retrieval_response.json()
    contexts = retrieval_data.get("contexts", [])

    # 🔹 Step 2: Handle empty retrieval (Hallucination control)
    if not contexts:
        return {
            "answer": "I don't know based on the provided documents.",
            "sources": []
        }

    # 🔹 Step 3: Build Prompt
    prompt = build_prompt(request.question, contexts)

    # 🔹 Step 4: Call LLM
    answer = generate_answer(prompt)

    used_sources = []

    for ctx in contexts:
        source_str = f"{ctx['metadata']['source']} (page {ctx['metadata']['page']})"
        if str(ctx["metadata"]["page"]) in answer:
            used_sources.append(source_str)

    used_sources = list(set(used_sources))

    return {
        "answer": answer,
        "sources": used_sources
    }
