import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("# About")
        st.markdown("""
        Elastic HealthCare is an AI-powered healthcare intelligence platform that combines Google Cloud’s Vertex AI and Elasticsearch to deliver real-time, multimodal, and multilingual insights from structured and unstructured medical data.
        """)
        st.markdown("---")
#         st.markdown(""" 
# # ⚙️ Key Features
# 🌐 **Multilingual Understanding**: Supports multiple languages for global healthcare teams.

# 🔍 **Hybrid Search**: Seamlessly integrates structured and unstructured medical data.

# 💬 **Conversational Interface**: Natural language querying powered by Gemini + Elasticsearch.

# 🔒 **Secure & Compliant**: Built on Elastic Cloud with fine-grained access control and monitoring.

# 📊 **Real-Time Observability**: Track data performance and model behavior with Elastic Observability."""
#         )
#         st.markdown("---")

#         st.markdown(
#             """# FAQ
# ### ❓1. What is Elastic HealthCare?

# Elastic HealthCare is an AI-driven healthcare platform that combines Google Cloud’s Vertex AI (Gemini) and Elasticsearch to make healthcare data searchable, conversational, and intelligent. It allows doctors, researchers, and analysts to query and interpret multimodal and multilingual data securely in real time.

# ### ❓2. What problem does Elastic HealthCare solve?

# Healthcare data is vast and siloed — scattered across medical reports, clinical notes, and imaging systems. Elastic HealthCare breaks these silos using hybrid search and GenAI, enabling quick insights from both structured and unstructured data while maintaining privacy and compliance.

# ### ❓3. How does it use Elasticsearch and Google Cloud?

# Elasticsearch provides powerful hybrid search and vector retrieval across patient records and documents.

# Google Cloud’s Vertex AI (Gemini) powers natural language understanding, summarization, and multimodal analysis.

# Together, they enable search, chat, and insights from complex healthcare datasets in a unified experience.

# ### ❓4. What makes Elastic HealthCare unique?

# Integrates multimodal data (text, images, reports).

# Supports multilingual queries for global healthcare access.

# Uses private-context-aware GenAI for secure, domain-specific intelligence.

# Provides end-to-end observability and monitoring with Elastic Observability.
# """
#         )