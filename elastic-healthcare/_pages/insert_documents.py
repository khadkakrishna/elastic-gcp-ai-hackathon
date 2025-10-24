import streamlit as st
import os
from google import genai
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import uuid

load_dotenv()

# --- Initialize clients ---
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTIC_API_KEY"),
)

INDEX_NAME = "medquad_index_with_embeddings_gemini"

st.set_page_config(page_title="Insert Q&A", layout="wide")
st.markdown("### 📝 Add Question & Answer to Knowledge Base")
st.markdown("Enter a **question** and **answer**, and optionally fill additional metadata.")

# --- Form for input ---
with st.form(key="qa_form"):
    # Required fields
    question = st.text_area("Question *", help="This field is required")
    answer = st.text_area("Answer *", help="This field is required")

    # Optional fields inside an expander
    with st.expander("Optional Metadata"):
        document_id = st.text_input("Document ID (optional)")
        source = st.text_input("Source")
        url = st.text_input("Source URL")
        question_id = st.text_input("Question ID")
        question_type = st.selectbox("Question Type", ["", "factoid", "list", "yes/no", "other"])
        focus = st.text_input("Focus")
        cuis = st.text_area("CUIs (comma-separated)")
        semantic_types = st.text_area("Semantic Types (comma-separated)")
        semantic_group = st.text_input("Semantic Group")
        synonyms = st.text_area("Synonyms (comma-separated)")

    submitted = st.form_submit_button("Add to Knowledge Base")

if submitted:
    if not question or not answer:
        st.error("❌ Question and Answer are required fields.")
    else:
        try:
            # --- Generate embeddings ---
            question_emb = client.models.embed_content(
                model="gemini-embedding-001",
                contents=question
            ).embeddings[0].values

            answer_emb = client.models.embed_content(
                model="gemini-embedding-001",
                contents=answer
            ).embeddings[0].values

            # --- Prepare document ---
            doc = {
                "document_id": document_id or str(uuid.uuid4()),
                "source": source or "",
                "url": url or "",
                "focus": focus or "",
                "cuis": [c.strip() for c in cuis.split(",")] if cuis else [],
                "semantic_types": [s.strip() for s in semantic_types.split(",")] if semantic_types else [],
                "semantic_group": semantic_group or "",
                "synonyms": [s.strip() for s in synonyms.split(",")] if synonyms else [],
                "question_id": question_id or "user_input",
                "question_type": question_type or "",
                "question": question,
                "answer": answer,
                "file_path": "user_input",
                "question_embedding": question_emb,
                "answer_embedding": answer_emb
            }

            # --- Index into Elasticsearch ---
            es.index(index=INDEX_NAME, document=doc)
            st.success(f"✅ Q&A added successfully! Document ID: {doc['document_id']}")

        except Exception as e:
            st.error(f"⚠️ Failed to index Q&A: {e}")
