import streamlit as st
import utils

st.markdown("""
### ⚖️ Reranking Search Results
Refine your search results using **text similarity reranking** powered by **Vertex AI**.
""")

query_text = st.text_input("Enter your query:", placeholder="e.g., Treatments for Parkinson disease?")
index_name = st.text_input("Elasticsearch index name:", value="medquad_qa")
rank_window_size = st.slider("Rank window size (top-K docs to rerank):", 1, 50, 10)
min_score = st.number_input("Minimum relevance score:", value=0.6, step=0.1)

if st.button("🔍 Run Reranking Search"):
    if not query_text.strip():
        st.warning("Please enter a query first.")
    else:
        resp = utils.rerank_documents(index_name, query_text, rank_window_size, min_score)

        if resp and "hits" in resp and "hits" in resp["hits"]:
            hits = resp["hits"]["hits"]
            if hits:
                results = []
                for hit in hits:
                    results.append({
                        "ID": hit.get("_id", ""),
                        "Score": round(hit.get("_score", 0.0), 3),
                        "Text": hit["_source"].get("answer", "") + "..."
                    })
                st.success(f"✅ Found {len(results)} reranked documents")
                st.dataframe(results)
            else:
                st.info("No results found after reranking.")
        else:
            st.error("Unexpected response format from Elasticsearch or empty response.")
