import uuid

import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="industrial_knowledge"
)


def store_chunks(chunks, filename):
    document_id = str(uuid.uuid4())

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "filename": filename,
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    embeddings = model.encode(documents)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(ids)


def search_chunks(question, n_results=3):
    query_embedding = model.encode([question])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results