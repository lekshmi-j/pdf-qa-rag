import faiss
import os
import pickle
import numpy as np

VECTOR_DIR = "vector_store"
INDEX_PATH = f"{VECTOR_DIR}/index.faiss"
META_PATH = f"{VECTOR_DIR}/meta.pkl"

def store_embeddings(embeddings, metadata):
    os.makedirs(VECTOR_DIR, exist_ok=True)

    dim = embeddings.shape[1]

    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            meta_store = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(dim)
        meta_store = []

    index.add(np.array(embeddings).astype("float32"))
    meta_store.extend(metadata)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta_store, f)
