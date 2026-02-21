import re

def clean_chunk_text(text: str) -> str:
    # Remove patterns like [Chunk 1#page6]
    return re.sub(r"\[Chunk\s*\d+#page\d+\]", "", text).strip()


def build_prompt(question: str, contexts: list):

    cleaned_contexts = []

    for i, ctx in enumerate(contexts):
        raw_text = ctx["text"]
        cleaned_text = clean_chunk_text(raw_text)

        source = ctx["metadata"]["source"]
        page = ctx["metadata"]["page"]

        formatted = f"""
        Source: {source} (page {page})
        Content:
        {cleaned_text}
        """

        cleaned_contexts.append(formatted)

    joined_context = "\n\n---\n\n".join(cleaned_contexts)

    prompt = f"""
You are an assistant answering questions strictly from the provided context.

Rules:
- Answer ONLY using the context below.
- If answer is not found, say "I don't know."
- Cite sources in format: (filename page X)
- Do NOT include chunk numbers

Context:
{joined_context}

Question:
{question}

Answer:
"""

    return prompt