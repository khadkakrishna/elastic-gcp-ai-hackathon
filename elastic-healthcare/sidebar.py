import streamlit as st

def sidebar():
    with st.sidebar:
        st.image(
            image="assets/main.png",
        )

        st.markdown("### About")
        st.markdown("""
        Elastic HealthCare is an AI-powered healthcare intelligence platform that combines Google Cloud’s Vertex AI and Elasticsearch to deliver real-time, multimodal, and multilingual insights from structured and unstructured medical data.
        """)
        st.markdown("---")
        st.caption("Built with ❤️ using Elasticsearch, GCP(Vertex AI and Gemini), and Streamlit.")
        st.caption("© 2025 Krishna Khadka | krishnakhadka2802@gmail.com")
