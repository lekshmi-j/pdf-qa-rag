import streamlit as st
import requests
import json

INGESTION_URL = "http://localhost:8000/upload"
ANSWER_URL = "http://localhost:8002/answer"

st.set_page_config(page_title="PDF RAG System")

st.title("📄 PDF Question Answering System")

# -----------------------------
# PDF Upload    
# -----------------------------
st.header("Upload PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

    with st.spinner("Uploading and indexing..."):
        try:
            response = requests.post(INGESTION_URL, files=files)
            if response.status_code == 200:
                st.success("PDF uploaded and indexed successfully.")
            else:
                st.error("Upload failed.")
        except Exception as e:
            st.error(f"Upload error: {str(e)}")


# -----------------------------
# Ask Question
# -----------------------------
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Get Answer"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        status_placeholder=st.empty()
        
        try:
            status_placeholder.info("Retrieving context and preparing answer...")
            response = requests.post(
                ANSWER_URL,
                json={
                    "question": question,
                    "top_k": 2
                },
                stream=True,
                timeout=None
            )

            if response.status_code != 200:
                st.error("Failed to generate answer.")
            else:
                status_placeholder.success("Answer generation in progress...")
                st.subheader("Answer")
                answer_placeholder = st.empty()
                sources_placeholder=st.empty()

                full_answer = ""

                # Stream line by line
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))

                        # Streaming tokens
                        if data["type"] == "token":
                            full_answer += data["content"]
                            answer_placeholder.markdown(full_answer + "▌")  # Add cursor

                        # Sources arrive after completion
                        elif data["type"] == "sources":
                            sources_placeholder.markdown("### Sources")
                            for src in data["content"]:
                                sources_placeholder.markdown(f"- {src}")

                        # Done signal
                        elif data["type"] == "done":
                            break

                        # Error signal
                        elif data["type"] == "error":
                            st.error(data["content"])
                            break
                answer_placeholder.markdown(full_answer)
                status_placeholder.empty()

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")