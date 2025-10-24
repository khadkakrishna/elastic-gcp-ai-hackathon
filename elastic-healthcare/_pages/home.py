import streamlit as st
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Elastic HealthCare",
    page_icon="🩺",
    layout="wide",
)

# --- HEADER SECTION ---
st.title("Elastic HealthCare 🩺")
st.subheader("Smarter Insights. Better Care.")
st.write(
    "Elastic HealthCare is an AI-powered healthcare intelligence platform that combines "
    "Google Cloud Vertex AI and Elasticsearch to bring real-time, multimodal, and multilingual insights "
    "from structured and unstructured healthcare data."
)

# --- IMAGE / BANNER ---
# st.image("_pages/assets/banner.png", use_container_width=True)

# --- FEATURE HIGHLIGHTS ---
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


# --- FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ using Elasticsearch, Vertex AI (Gemini), and Streamlit.")
st.caption("© 2025 Elastic HealthCare | Hackathon Edition")
