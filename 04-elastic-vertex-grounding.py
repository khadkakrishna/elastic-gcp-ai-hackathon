from google import genai
from google.genai.types import (
    GenerateContentConfig,
    ExternalApi,
    Retrieval,
    Tool,
    HttpOptions,
)
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"]="True"
os.environ["GOOGLE_API_KEY"] = os.getenv("VERTEX_AI_API_KEY")

client = genai.Client(http_options=HttpOptions(api_version="v1"))

# Replace with your Elasticsearch details
ELASTIC_SEARCH_ENDPOINT = os.getenv("ELASTICSEARCH_URL")
ELASTIC_SEARCH_API_KEY = os.getenv("ELASTIC_API_KEY")
INDEX_NAME = "medquad_index_with_embeddings_gemini"
SEARCH_TEMPLATE_NAME = "google-template-knn-multioutput"
NUM_HITS = 5

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
    model="gemini-2.5-flash",  
    contents="What are the treatments for Chronic Fatigue Syndrome (CFS)",
    config=GenerateContentConfig(
        tools=[tool],
    ),
)

print(response.text)