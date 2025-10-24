import streamlit as st
import sidebar
import utils

sidebar.sidebar()

pages = {
   "Home": [
         st.Page("_pages/home.py", title="Home"),
       ],
    "Elasticsearch": [
        st.Page("_pages/search_documents.py", title="Search from Elasticsearch"),
        st.Page("_pages/insert_documents.py", title="Insert documents into Elasticsearch"),
        ],
    "Vertex AI": [
        st.Page("_pages/vertex_ai_grounding.py", title="Vertex AI Grounding"),
        ],    
    "Observability": [
        st.Page("_pages/observability.py", title="Observability"),
        ],
}

pg = st.navigation(pages, position="top")
pg.run()

