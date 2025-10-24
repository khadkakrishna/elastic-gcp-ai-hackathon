import streamlit as st

import streamlit.components.v1 as components

st.set_page_config(page_title="Observability", layout="wide")

st.title("🔎 Vertex AI Observability Dashboard")
st.markdown("""
Monitor **Vertex AI grounding metrics** and performance data stored in **Elasticsearch**.
Use this dashboard to track trends, latency, and usage of your AI models.
""")

components.iframe(src="https://test-cluster-bd5f7a.kb.us-central1.gcp.cloud.es.io/s/observability-space/app/dashboards#/view/gcp_vertexai-1b42c117-7971-424d-8015-c02f1317824d?embed=true&_g=%28refreshInterval%3A%28pause%3A%21t%2Cvalue%3A60000%29%2Ctime%3A%28from%3Anow-15d%2Cto%3Anow%29%29", 
                  height=800, 
                  width=1200,
                  scrolling=True)

