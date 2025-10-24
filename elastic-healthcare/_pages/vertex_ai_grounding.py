import streamlit as st
import utils
import html

st.markdown(
    """
    ### 🤖 Vertex AI Grounding
    Ask a question and get responses from Vertex AI using grounding data from Elasticsearch.
    """
)

# Query input
question = st.text_input("Enter your question:")

# Model selection
model_name = st.selectbox(
    "Select Vertex AI Model",
    options=["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"],
    index=0,  # Default is gemini-2.5-flash
    help="Choose the model to use for generating answers."
)

col1, col2 = st.columns(2)

if col1.button("Get response from Vertex AI"):
    if not question:
        st.warning("Please enter a question.")
    else:
        try:
            resp = utils.get_response_from_vertex_ai(question, model=model_name)
            
            if resp:
                grounding_docs = []
                candidates = resp.candidates
                if resp.candidates is None:
                    st.info("No grounding candidates found.")
                else:
                    for candidate in candidates:
                        grounding_supports = resp.candidates[0].grounding_metadata.grounding_supports

                        for support in grounding_supports:
                            segment_text = support.segment.text
                            grounding_docs.append(segment_text)
                        
                st.subheader("💡 Vertex AI Response")
                st.markdown(resp.text)
                
                if grounding_docs and len(grounding_docs) > 0:
                    st.subheader("📚 Grounding Documents")
                    for doc in grounding_docs[:5]:  # show only first 5
                        truncated = " ".join(doc.split()[:5]) + "…"  # first 5 words
                        escaped_doc = html.escape(doc)  # escape special characters
                        st.markdown(
                            f'- <a href="#{escaped_doc}" style="color:blue" target="_blank" title="{escaped_doc}">{truncated}</a>',
                            unsafe_allow_html=True
                        )

                else:
                    st.info("No grounding documents found in elasticsearch.")
            else:
                st.info("No response received from Vertex AI.")
        except Exception as e:
            st.error(f"⚠️ Error fetching response: {e}")
