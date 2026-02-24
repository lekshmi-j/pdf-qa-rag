**📄 PDF RAG Q&A System**
Production-Style Retrieval-Augmented Generation with Microservice Architecture
**🚀 Overview**

This project implements a production-oriented Question Answering system over PDFs using Retrieval-Augmented Generation (RAG).

Unlike notebook-based prototypes, this system is intentionally built with:

        Microservice-style architecture
        
        Independent REST APIs
        
        Vector search infrastructure
        
        Hallucination control mechanisms
        
        Docker-based deployment
        
        Frontend client integration

The goal is to simulate how real-world AI knowledge assistants are built inside companies (legal, HR, finance, internal documentation tools).

**🎯 Problem Statement**

Build a scalable and modular system that allows users to:

Upload PDFs → Ask questions → Receive grounded answers with citations

The system must:

        Avoid hallucinations as much as possible
        
        Separate ingestion, retrieval, and generation
        
        Be deployable and production-aware
        
        Be explainable in interviews

**🏗️ System Architecture**

        Client (Streamlit Frontend)
                |
                v
        -------------------------------
        |   API-based Service Layer   |
        -------------------------------
                |
                v
        ---------------------------------------------------
        | Ingestion Service | Retrieval Service | RAG LLM |
        ---------------------------------------------------
                |
                v
               Vector Database (FAISS / Chroma)

**Design Principles:**

Single responsibility per service

Clear separation of concerns

REST-based communication

Embedding & retrieval decoupled from generation

Designed for independent scaling

🧩 **Microservices Breakdown**
**🔹 1. Document Ingestion Service**

Responsibility:
        PDF → Clean text → Chunking → Embeddings → Vector storage

This service:

        Never calls an LLM
        
        Never answers questions
        
        Only prepares knowledge

Key Concepts Implemented

        PDF parsing (PyMuPDF / pdfplumber)
        
        Multiple chunking strategies
        
        Fixed-size chunks
        
        Overlapping chunks
        
        Metadata tracking (source, page, chunk_id)
        
        Sentence-transformer embeddings
        
        Vector persistence


**Endpoints**

        POST /upload

**2. Retrieval Service**

Responsibility:
        User query → Embedding → Top-k semantic search

This service:

        Never parses PDFs
        
        Never generates answers
        
        Only retrieves relevant context

Concepts Implemented

        Cosine similarity search
        
        Top-k tuning
        
        Score threshold filtering
        
        Metadata-based filtering
        
        Retrieval evaluation logic

Why This Matters

Retrieval quality directly determines answer quality.
Most RAG failures originate from poor retrieval, not the LLM.

**Endpoint**

        POST /retrieve

Returns:

Relevant chunks

Similarity scores

Metadata

**3. RAG / LLM Service**

Responsibility:
        Context + Question → Grounded answer

This service:

        Does not store embeddings
        
        Does not parse PDFs
        
        Only generates answers from retrieved context
        
        Hallucination Control Techniques
        
        Context-only prompting
        
        Explicit abstention instructions (“If not found, say I don’t know”)
        
        Source citation enforcement
        
        Temperature control
        
        Context window management

**Prompt Engineering Strategy**

The model is instructed to:

        Answer strictly from provided context
        
        Avoid external knowledge
        
        Cite document sources
        
        Admit uncertainty when context is insufficient

Endpoint
        POST /answer

Returns:

Generated answer

Source references

**🖥️ Frontend**

Streamlit-based UI that:

Uploads documents

Sends queries

Displays answers with sources

Interacts only via APIs

Contains zero business logic

This maintains strict client–server separation.

**🧠 Core RAG Concepts Demonstrated**

        Chunking strategy trade-offs
        
        Embedding similarity search
        
        Top-k sensitivity analysis
        
        Retrieval vs generation responsibilities
        
        Context window limits
        
        Hallucination mitigation
        
        Prompt discipline
        
        API-first system design

**🛠️ Tech Stack**

| Layer        | Technology                              |
| ------------ | --------------------------------------- |
| Backend APIs | FastAPI                                 |
| Embeddings   | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector DB    | FAISS / Chroma                          |
| LLM          | HuggingFace API / Open models           |
| Frontend     | Streamlit                               |
| Deployment   | Docker + Docker Compose                 |
| Language     | Python                                  |


**🐳 Deployment Architecture**

Each service:

Has its own Dockerfile

Can be deployed independently

Is orchestrated using docker-compose

This mirrors how production AI services are deployed.

Example deployment strategy:

Backend services → Render / Fly.io / Railway (free tier)

Frontend → Streamlit Cloud

**📁 Repository Structure**

pdf-rag-microservices/
│
├── services/
│   ├── ingestion_service/
│   ├── retrieval_service/
│   └── rag_service/
│
├── frontend/
│
├── docker-compose.yml
├── README.md
└── architecture.png

**📈 Engineering Decisions**
**Why Microservices?**

Embedding models may change without affecting generation

Vector DB can be swapped independently

Retrieval tuning doesn’t break LLM service

Enables independent scaling

**🧪 How to Run**
