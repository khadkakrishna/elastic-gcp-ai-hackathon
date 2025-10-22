from elasticsearch import Elasticsearch
from google import genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTIC_API_KEY"),
)

INDEX_NAME = "medquad_index_with_embeddings_gemini"
query_text = "Treatments for Parkinson disease?"

query_embedding = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query_text
).embeddings[0].values 

query_vector_json = json.dumps(query_embedding) 

resp = es.search_template(
    index=INDEX_NAME,
    body={
        "id": "knn_search_template",
        "params": {
            "query_vector": query_vector_json,
            "k": 1,
            "num_candidates": 50
        }
    }
)

for hit in resp["hits"]["hits"]:
    print(f"\nID: {hit['_id']}")
    print(f"Question: {hit['_source']['question']}")
    print(f"Answer: {hit['_source']['answer']}")
