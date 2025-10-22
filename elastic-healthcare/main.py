import streamlit as st
import sidebar
import utils

sidebar.sidebar()

st.title("🩺 Elastic Healthcare")
st.markdown(
   """
   Smarter Insights for Better Care.
   Enter your name in the text box below and press a button to see some fun features in Streamlit.
   """
)

name = st.text_input("Enter your name please:")


# Use columns to create buttons side by side
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