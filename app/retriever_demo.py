from qdrant_client.http.exceptions import UnexpectedResponse

from langchain_community.vectorstores import FAISS
from .config import settings
from .ingestion.embeddings import EmbeddingProvider
from .ingestion.indexer import faiss_load_for_tenant, qdrant_pooled_search

def demo_query(tenant_id: str, query: str, mode: str = "HYBRID", k: int = 3):
    emb = EmbeddingProvider(settings.openai_api_key)
    mode = mode.upper()

    if mode == "SILOED":
        vs: FAISS = faiss_load_for_tenant(tenant_id, emb)
        return vs.similarity_search(query, k=k)

    elif mode == "POOLED":
        return qdrant_pooled_search(query, tenant_id, k, emb)

    else:  # HYBRID demo: try siloed first, else pooled
        try:
            vs = faiss_load_for_tenant(tenant_id, emb)
            return vs.similarity_search(query, k=k)
        except Exception:
            return qdrant_pooled_search(query, tenant_id, k, emb)

if __name__ == "__main__":
    from pprint import pprint
    for tenant in ("tenantA", "tenantB"):
        res = demo_query(tenant, "What is the SLA?", mode="HYBRID")
        print(f"\n=== {tenant} ===")
        for r in res:
            pprint({"text": r.page_content[:120], "meta": r.metadata})
