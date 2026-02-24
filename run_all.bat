@echo off

echo ==========================================
echo Starting Ingestion Service...
echo ==========================================
start cmd /k "cd services\ingestion_service && ingestion_env\Scripts\activate && uvicorn main:app --port 8000 --reload"

echo ==========================================
echo Starting Retrieval Service...
echo ==========================================
start cmd /k "cd services\retrieval_service && retrieval_env\Scripts\activate && uvicorn main:app --port 8001 --reload"

echo ==========================================
echo Starting RAG Service...
echo ==========================================
start cmd /k "cd services\rag_service && rag_env\Scripts\activate && uvicorn main:app --port 8002 --reload"

echo ==========================================
echo Starting Streamlit Frontend...
echo ==========================================
start cmd /k "cd frontend && venv\Scripts\activate && streamlit run streamlit_app.py"

echo All services launched.