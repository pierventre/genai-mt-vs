import os
from typing import Iterable
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from .embeddings import EmbeddingProvider
from ..config import settings

# --- Siloed (FAISS per tenant) ---
def faiss_save_for_tenant(tenant_id: str, docs: list[Document], emb: EmbeddingProvider):
    path = f"indexes/{tenant_id}"
    os.makedirs(path, exist_ok=True)
    vs = FAISS.from_documents(docs, emb.embedding_fn())
    vs.save_local(path)
    return path

def faiss_load_for_tenant(tenant_id: str, emb: EmbeddingProvider) -> FAISS:
    path = f"indexes/{tenant_id}"
    return FAISS.load_local(path, emb.embedding_fn(), allow_dangerous_deserialization=True)

# --- Pooled (Qdrant with tenant_id filter) ---
_qdrant_client = QdrantClient(":memory:")  # demo; replace with http://localhost:6333 for real server
_qdrant_client.delete_collection(settings.qdrant_collection)

def qdrant_pooled_add(docs: Iterable[Document], emb: EmbeddingProvider):
    vs = QdrantVectorStore(_qdrant_client, collection_name=settings.qdrant_collection, embedding=emb.embedding_fn())
    vs.add_documents(list(docs))

def qdrant_pooled_search(query: str, tenant_id: str, k: int, emb: EmbeddingProvider):
    vs = QdrantVectorStore(_qdrant_client, collection_name=settings.qdrant_collection, embedding=emb.embedding_fn())
    qfilter = Filter(
        must=[
            {"key": "tenant_id", "match": {"value": tenant_id}}
        ]
    )
    return vs.similarity_search(query, k=k, filter=qfilter)
