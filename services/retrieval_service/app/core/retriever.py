import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

VECTOR_PATH = "../ingestion_service/vector_store"
INDEX_PATH = os.path.join(VECTOR_PATH, "index.faiss")
META_PATH = os.path.join(VECTOR_PATH, "meta.pkl")

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, top_k=5, score_threshold=None, source_filter=None):
    # print(f"Retrieving for query: '{query}' with top_k={top_k}, score_threshold={score_threshold}, source_filter='{source_filter}'")
    if not os.path.exists(INDEX_PATH):
        return []

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata_store = pickle.load(f)

    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(distances[0], indices[0]):
        metadata = metadata_store[idx]

        if idx == -1:
            continue

        # Apply source filter safely
        if source_filter is not None and source_filter != "":
            if metadata.get("source") != source_filter:
                continue

        # Apply score threshold safely (L2 distance: smaller = better)
        if score_threshold is not None and score > score_threshold:
                continue

        results.append({
            "score": float(score),
            "metadata": metadata
        })

    return results
