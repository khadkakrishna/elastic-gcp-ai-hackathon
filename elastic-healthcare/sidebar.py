import streamlit as st

def sidebar():
    with st.sidebar:
        st.image(
            image="assets/main.png",
        )

        st.markdown("---")
        st.caption("Built with ❤️ using Elasticsearch, GCP(Vertex AI and Gemini), and Streamlit.")
        st.caption("© 2025 Krishna Khadka | krishnakhadka2802@gmail.com")
