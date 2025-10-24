import streamlit as st
import sidebar

sidebar.sidebar()

st.set_page_config(
    page_title="Elastic HealthCare", 
    page_icon="assets/logo.jpeg", 
    layout="wide" 
)


pages = {
   "Home": [
         st.Page("_pages/home.py", title="Home"),
       ],
    "Elasticsearch": [
        st.Page("_pages/search_documents.py", title="Search from Knowledge Base"),
        st.Page("_pages/insert_documents.py", title="Insert into Knowledge Base"),
        st.Page("_pages/rerank_documents.py", title="Reranking Documents"),
        ],
    "Vertex AI": [
        st.Page("_pages/vertex_ai_grounding.py", title="Vertex AI Grounding Source"),
        ],    
    "Observability": [
        st.Page("_pages/observability.py", title="Observability"),
        ],
}

pg = st.navigation(pages, position="top")
pg.run()

