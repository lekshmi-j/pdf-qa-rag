
import faiss

index = faiss.read_index("../vector_store/index.faiss")
print("Total vectors:", index.ntotal)
