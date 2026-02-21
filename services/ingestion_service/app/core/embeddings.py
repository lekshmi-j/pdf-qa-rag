from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks, source):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts)

    metadata = []
    for c in chunks:
        metadata.append({
            "text": c["text"],
            "source": source,
            "page": c["page"],
            "chunk_id": c["chunk_id"]
        })

    return embeddings, metadata
