from elasticsearch import Elasticsearch
import json
from dotenv import load_dotenv
import os
load_dotenv()
client = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTIC_API_KEY"),
)

retriever_object = {
    "standard": {
        "query": {
            "multi_match": {
                "query": "Can u tell me more about Aarskog-Scott syndrome",
                "fields": [
                    "answer", "question"
                ]
            }
        }
    }
}

search_response = client.search(
    index="medquad_index_with_embeddings_gemini",
    retriever=retriever_object,
    size=3
)

for hit in search_response["hits"]["hits"]:
    print(hit["_source"]["question"])
    print(hit["_source"]["answer"])
    print("-----")