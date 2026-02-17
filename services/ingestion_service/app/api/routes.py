from fastapi import APIRouter, UploadFile, File
from app.core.pdf_loader import extract_text_from_pdf
from app.core.chunker import fixed_chunking, overlapping_chunking
from app.core.embeddings import embed_chunks
from app.core.vector_store import store_embeddings
import os
import aiofiles

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    pages = extract_text_from_pdf(file_path)

    chunks = overlapping_chunking(pages)
    embeddings, metadata = embed_chunks(chunks, source=file.filename)

    store_embeddings(embeddings, metadata)

    return {"message": "PDF ingested", "chunks": len(chunks)}


@router.post("/reindex")
def reindex():
    # later: loop over all PDFs and rebuild index
    return {"message": "Reindexing triggered"}
