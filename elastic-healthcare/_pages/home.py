import streamlit as st

st.set_page_config(
    page_title="Elastic HealthCare",
    layout="wide",
)

st.markdown("## Verified medical answers, Trusted by doctors, powered by AI 🩺")
st.write(
    "Elastic HealthCare is an AI-powered healthcare intelligence platform that combines "
    "Google Cloud Vertex AI and Elasticsearch to bring real-time, multimodal, and multilingual insights "
    "from structured and unstructured healthcare data."
)

st.markdown("### Key Features ✨")

cols = st.columns(3)
with cols[0]:
    st.markdown("""
    - 🔍 **Hybrid Search**  
      Search across structured & unstructured medical data.
    - 💬 **Conversational Assistant**  
      Chat with AI to summarize records and reports.
    """)
with cols[1]:
    st.markdown("""
    - 🌐 **Multilingual & Multimodal**  
      Understands multiple languages and data types (text, images, PDFs).
    - 📊 **AI Insights Dashboard**  
      Real-time analytics powered by Elastic Observability.
    """)
with cols[2]:
    st.markdown("""
    - 🔒 **Secure & Compliant**  
      HIPAA-ready design with Elastic Security and IAM integration.
    - ☁️ **Google Cloud Integration**  
      Vertex AI, GCS, and Elastic Cloud working together.
    """)
    

st.divider()
st.markdown("#### 💡 Try asking one of these questions:")

suggestions = [
    "what are symptoms of book syndrome?",
    "Can u tell me about Gliomatosis cerebri?",
    "Is Glass-Chapman-Hockley syndrome inherited?",
    "Can u tell me more about Aarskog-Scott syndrome?",
    "What are the treatments for Chronic Fatigue Syndrome (CFS)?"
]

for i in suggestions:
    st.markdown(f"- {i}")

st.divider()
