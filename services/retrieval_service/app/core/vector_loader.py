import faiss
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTOR_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../../ingestion_service/vector_store")
)

INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_DIR, "meta.pkl")


def load_vector_store():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("FAISS index not found.")

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
