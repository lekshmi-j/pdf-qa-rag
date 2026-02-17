from app.utils.text_cleaner import clean_text

def fixed_chunking(pages, chunk_size=500):
    chunks = []
    chunk_id = 0

    for page in pages:
        text = clean_text(page["text"])
        words = text.split()

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append({
                "text": chunk,
                "page": page["page"],
                "chunk_id": chunk_id
            })
            chunk_id += 1

    return chunks


def overlapping_chunking(pages, chunk_size=500, overlap=100):
    chunks = []
    chunk_id = 0

    for page in pages:
        text = clean_text(page["text"])
        words = text.split()

        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append({
                "text": chunk,
                "page": page["page"],
                "chunk_id": chunk_id
            })
            chunk_id += 1
            i += chunk_size - overlap

    return chunks
