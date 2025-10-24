import streamlit as st
import utils

st.markdown(
   """
   ### 🔍 Smarter Search and Insights for Better Care.
   
   Enter your query in the text box below and click on the button you want to get results for .
   """
)

# Query input
name = st.text_input("Enter your query please:")

# Parameters
k = st.slider("Select top-k results:", min_value=1, max_value=10, value=3, step=1)
num_candidates = st.number_input("Number of candidates to consider:", min_value=1, value=50, step=1)

col1, col2 = st.columns(2)

if col1.button("Get answers from Elasticsearch!"):
    # Pass k and num_candidates to your utils function
    resp = utils.get_answers_from_elasticsearch(name, k=k, num_candidates=num_candidates)
    
    if resp and "hits" in resp and resp["hits"]["hits"]:
        results = []
        for hit in resp["hits"]["hits"]:
            results.append({
                "ID": hit["_id"],
                "Question": hit["_source"].get("question", ""),
                "Answer": hit["_source"].get("answer", "")
            })
        
        st.json(results)  # Display results as JSON
    else:
        st.info("No results found.")
