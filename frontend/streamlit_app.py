import streamlit as st
import requests

INGESTION_URL = "http://localhost:8000/upload"
ANSWER_URL = "http://localhost:8002/answer"

st.set_page_config(page_title="PDF RAG System")

st.title("📄 PDF Question Answering System")

# -------- PDF Upload --------
st.header("Upload PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

    with st.spinner("Uploading and indexing..."):
        response = requests.post(INGESTION_URL, files=files)

    if response.status_code == 200:
        st.success("PDF uploaded and indexed successfully.")
    else:
        st.error("Upload failed.")


# -------- Ask Question --------
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Get Answer"):

    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            response = requests.post(
                ANSWER_URL,
                json={
                    "question": question,
                    "top_k": 3
                }
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")
            for src in data["sources"]:
                st.write(f"- {src}")

        else:
            st.error("Failed to generate answer.")