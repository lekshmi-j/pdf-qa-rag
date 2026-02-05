# PDF RAG Q&A System
## Problem Statement
Build a production-style Question Answering system over PDFs using
Retrieval-Augmented Generation (RAG), designed with microservices,
scalable APIs, and deployment in mind.

This project intentionally avoids notebook-only prototypes and focuses
on real-world engineering practices.

## High-Level Architecture

Client (Streamlit / Web UI)
        |
        v
API Gateway / Client Layer
        |
        v
-------------------------------------------
| Ingestion | Retrieval | RAG Generation |
-------------------------------------------
        |
        v
     Vector Database

Each service:
- Single responsibility
- Independent FastAPI app
- Dockerized
- Communicates via REST

## Why Microservices?
- Clear separation of concerns
- Independent scaling
- Easier debugging and testing
- Mirrors real production RAG systems

## Tech Stack
- Python
- FastAPI
- Docker & Docker Compose
- Vector DB (TBD)
- LLM API (TBD)
- Streamlit (Frontend)

## Current Status
Phase 0: Project framing and repository setup.

## Limitations (Intentional)
- No auth (yet)
- No monitoring (yet)
- Single-user assumption
- Not optimized for cost

These will be addressed incrementally.
