import streamlit as st
import sidebar
import utils

sidebar.sidebar()

st.title("🩺 Elastic Healthcare")
st.markdown(
   """
   ### Smarter Insights for Better Care.
   
   Enter your query in the text box below and click on the button you want to get results for.
   """
)

name = st.text_input("Enter your query please:")


col1, col2 = st.columns(2)

ans = ""
with col1:
   if st.button("Get embeddings!"):
      ans = utils.get_embedding(name)

with col2:
   if st.button("Get answers from Elasticsearch!"):
      
      ans = utils.get_answers_from_elasticsearch(name)
st.write(f"{name}")
st.write(ans)