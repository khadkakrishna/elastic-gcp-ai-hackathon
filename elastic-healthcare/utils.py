from google import genai
from elasticsearch import Elasticsearch
import json
import os
from google.genai.types import (
    GenerateContentConfig,
    ExternalApi,
    Retrieval,
    Tool,
    HttpOptions
)
from dotenv import load_dotenv
load_dotenv()

ELASTIC_SEARCH_ENDPOINT = os.getenv("ELASTICSEARCH_URL")
ELASTIC_SEARCH_API_KEY = os.getenv("ELASTIC_API_KEY")
INDEX_NAME = "medquad_index_with_embeddings_gemini"
SEARCH_TEMPLATE_NAME = "google-template-knn-multioutput"
NUM_HITS = 5

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTIC_API_KEY"),
)

def get_embedding(text):
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text)
    return result.embeddings[0].values

def get_answers_from_elasticsearch(query_text, k, num_candidates, multilingual_enabled, language_code=None):
    # query_text = "Treatments for Parkinson disease?"
    if multilingual_enabled:
        INDEX_NAME = "medquad_index_with_embeddings_gemini_multilingual"
        knn = {
            "field": "answer_embedding",
            "query_vector": get_embedding(query_text),
            "k": k,
            "num_candidates": num_candidates,
        }

        if language_code:
            knn["filter"] = {
                "term": {
                    "language": language_code,
                }
            }
            
        res =  es.search(index=INDEX_NAME, knn=knn)
        return res

    else:
        INDEX_NAME = "medquad_index_with_embeddings_gemini"

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
                    "k": k,
                    "num_candidates": num_candidates
                }
            }
        )
        return resp


def get_response_from_vertex_ai(query_text, model="gemini-2.5-flash"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"]="True"
    os.environ["GOOGLE_API_KEY"] = os.getenv("VERTEX_AI_API_KEY")

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    tool = Tool(
        retrieval=Retrieval(
            external_api=ExternalApi(
                api_spec="ELASTIC_SEARCH",
                endpoint=ELASTIC_SEARCH_ENDPOINT,
                api_auth={
                    "apiKeyConfig": {
                        "apiKeyString": f"ApiKey {ELASTIC_SEARCH_API_KEY}"
                    }
                },
                elastic_search_params={
                    "index": INDEX_NAME,
                    "searchTemplate": SEARCH_TEMPLATE_NAME,
                    "numHits": NUM_HITS,
                },
            )
        )
    )
    response = client.models.generate_content(
        model=model,  
        contents=query_text,
        config=GenerateContentConfig(
            # response_mime_type= "application/json",
            tools=[tool]
        ),
    )
    return response
