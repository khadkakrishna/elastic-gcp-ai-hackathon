import os
import xmltodict
from google import genai
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTIC_API_KEY"),
)

INDEX_NAME = "medquad_index_with_embeddings_gemini"

mapping = {
    "mappings": {
        "properties": {
            "document_id": {"type": "keyword"},
            "source": {"type": "keyword"},
            "url": {"type": "keyword"},
            "focus": {"type": "text", "analyzer": "english"},
            "cuis": {"type": "keyword"},
            "semantic_types": {"type": "keyword"},
            "semantic_group": {"type": "keyword"},
            "synonyms": {"type": "text", "analyzer": "english"},
            "question_id": {"type": "keyword"},
            "question_type": {"type": "keyword"},
            "question": {"type": "text", "analyzer": "english"},
            "answer": {"type": "text", "analyzer": "english"},
            "file_path": {"type": "keyword"},
            "question_embedding": {
                "type": "dense_vector",
                "dims": 3072,
                "index": True,
                "similarity": "cosine"
            },
            "answer_embedding": {
                "type": "dense_vector",
                "dims": 3072,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}

# Create index with mapping
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Created index: {INDEX_NAME}")
else:
    print(f"Index {INDEX_NAME} already exists.")


def parse_medquad_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        xml_dict = xmltodict.parse(f.read())
    
    doc = xml_dict.get("Document", {})
    base_info = {
        "document_id": doc.get("@id"),
        "source": doc.get("@source"),
        "url": doc.get("@url"),
        "focus": doc.get("Focus"),
        "file_path": file_path,
    }

    anns = doc.get("FocusAnnotations", {})
    umls = anns.get("UMLS", {})
    base_info["cuis"] = umls.get("CUIs", {}).get("CUI")
    base_info["semantic_types"] = umls.get("SemanticTypes", {}).get("SemanticType")
    base_info["semantic_group"] = umls.get("SemanticGroup")
    syns = anns.get("Synonyms", {}).get("Synonym")
    if isinstance(syns, list):
        base_info["synonyms"] = syns
    elif syns:
        base_info["synonyms"] = [syns]
    else:
        base_info["synonyms"] = []

    qa_pairs = doc.get("QAPairs", {}).get("QAPair", [])
    if not isinstance(qa_pairs, list):
        qa_pairs = [qa_pairs]

    docs = []
    for qa in qa_pairs:
        q = qa.get("Question", {})
        a = qa.get("Answer", "")
        docs.append({
            **base_info,
            "question_id": q.get("@qid"),
            "question_type": q.get("@qtype"),
            "question": q.get("#text"),
            "answer": a,
        })
    return docs

def index_medquad_one_by_one(base_folder):
    total_docs = 0
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".xml"):
                full_path = os.path.join(root, file)
                try:
                    parsed_docs = parse_medquad_xml(full_path)
                    for doc in parsed_docs:
                        # Generate Gemini embedding for each question
                        embedding_ques = client.models.embed_content(
                            model="gemini-embedding-001",
                            contents=doc["question"]
                        ).embeddings[0]
                        embedding_ans = client.models.embed_content(
                            model="gemini-embedding-001",
                            contents=doc["answer"]
                        ).embeddings[0]
                        doc["_source"] = {**doc, 
                                          "question_embedding": embedding_ques.values, 
                                          "answer_embedding": embedding_ans.values
                                        }
                        es.index(index=INDEX_NAME, document=doc["_source"])
                        total_docs += 1
                except Exception as e:
                    print(f"⚠️ Error parsing {file}: {e}")
    es.indices.refresh(index=INDEX_NAME)
    print(f"✅ Indexed {total_docs} Q&A pairs successfully!")

def index_medquad_bulk(base_folder, batch_size=50):
    total_docs = 0
    all_docs = []

    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".xml"):
                full_path = os.path.join(root, file)
                try:
                    parsed_docs = parse_medquad_xml(full_path)
                    all_docs.extend(parsed_docs)
                except Exception as e:
                    print(f"⚠️ Error parsing {file}: {e}")

    for i in range(0, len(all_docs), batch_size):
        batch = all_docs[i:i + batch_size]
        questions = [doc["question"] for doc in batch]
        answers = [doc["answer"] for doc in batch]

        try:
            ques_embeddings = client.models.embed_content(
                model="gemini-embedding-001",
                contents=questions
            ).embeddings

            ans_embeddings = client.models.embed_content(
                model="gemini-embedding-001",
                contents=answers
            ).embeddings

            actions = []
            for j, doc in enumerate(batch):
                doc["_source"] = {
                    **doc,
                    "question_embedding": ques_embeddings[j].values,
                    "answer_embedding": ans_embeddings[j].values
                }
                actions.append({
                    "_index": INDEX_NAME,
                    "_source": doc["_source"]
                })

            helpers.bulk(es, actions)
            total_docs += len(actions)
            print(f"✅ Indexed batch {i//batch_size + 1} ({len(actions)} docs)")

        except Exception as e:
            print(f"⚠️ Error embedding or indexing batch {i//batch_size + 1}: {e}")

    es.indices.refresh(index=INDEX_NAME)
    print(f"🎯 Completed indexing {total_docs} Q&A pairs successfully!")


index_medquad_bulk("./MedQuAD", batch_size=100)