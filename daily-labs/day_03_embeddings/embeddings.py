import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def embedding_retrieve(query: str, documents: list[dict], k: int = 5):
    doc_vecs = embed_texts([d["text"] for d in documents])
    query_vec = embed_texts([query])[0]
    scores = [cosine_sim(query_vec, v) for v in doc_vecs]
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [(d["id"], float(s)) for d, s in ranked[:k]]


def embed_texts(texts: list[str]):
    return model.encode(texts, convert_to_numpy=True)


# if __name__ == "__main__":
#     vecs = embed_texts(["vip discount"])
#     print(f"Shape: {vecs.shape}")
#     print(f"First 5 values: {vecs[0][:5]}")


# if __name__ == "__main__":
#     fixtures_path = Path(__file__).parent.parent / "day_02_persistence" / "fixtures" / "pgms.json"
#     with open(fixtures_path, "r") as f:
#         documents = json.load(f)

#     query = "special pricing for loyal customers" #higher hit to "discount calculation" than "order processing"
#     query = "verifying a person's spending cap" #no hit to discount calculation, but hit to order processing

#     print(f"Query: '{query}'\n")
#     print("Embedding-based ranking:")
#     for doc_id, score in embedding_retrieve(query, documents, k=3):
#         print(f"  {doc_id}: {score:.4f}")


import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "day_02_persistence"))
from search_db import retrieve_filtered

if __name__ == "__main__":
    fixtures_path = Path(__file__).parent.parent / "day_02_persistence" / "fixtures" / "pgms.json"
    with open(fixtures_path, "r") as f:
        documents = json.load(f)

    db_path = str(Path(__file__).parent.parent / "day_02_persistence" / "mydb.db")
    query = "special pricing for loyal customers"

    print(f"Query: '{query}'\n") #no hit to anything but embedding-based ranking should hit discount calculation more than order processing

    print("BM25 (Day 2, keyword match):")
    print(retrieve_filtered(db_path, query, k=3))

    print("\nEmbeddings (Day 3, meaning match):")
    for doc_id, score in embedding_retrieve(query, documents, k=3):
        print(f"  {doc_id}: {score:.4f}")