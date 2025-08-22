import argparse
from typing import Iterable
from qdrant_client.models import VectorParams, Distance
from .connectors import load_raw_docs
from .preprocess import preprocess
from .chunk import chunk
from .pii import annotate_chunk_metadata
from .embeddings import EmbeddingProvider
from .indexer import faiss_save_for_tenant, qdrant_pooled_add, _qdrant_client
from ..config import settings

def ensure_collection(emb: EmbeddingProvider):
    if not _qdrant_client.collection_exists(settings.qdrant_collection):
        _qdrant_client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def _ingest_docs(raw_docs: Iterable[dict]) -> dict[str, list]:
    """Returns dict tenant_id -> list[Document] (chunked)."""
    by_tenant = {}
    for raw in raw_docs:
        pre = preprocess(raw)
        chunks = [annotate_chunk_metadata(c) for c in chunk(pre)]
        by_tenant.setdefault(pre["tenant_id"], []).extend(chunks)
    return by_tenant

def run_ingestion(data_dir: str):
    emb = EmbeddingProvider(settings.openai_api_key)
    by_tenant = _ingest_docs(load_raw_docs(data_dir))
    print(f"Prepared chunks for tenants: { {k: len(v) for k,v in by_tenant.items()} }")

    if settings.storage_mode == "SILOED":
        for tenant, chunks in by_tenant.items():
            path = faiss_save_for_tenant(tenant, chunks, emb)
            print(f"[SILOED] Tenant {tenant} -> FAISS saved at {path}")

    elif settings.storage_mode == "POOLED":
        # Ensure tenant_id in metadata for all chunks
        all_chunks = []
        for tenant, chunks in by_tenant.items():
            for c in chunks:
                c.metadata["tenant_id"] = tenant
                all_chunks.append(c)
        ensure_collection(emb)
        qdrant_pooled_add(all_chunks, emb)
        print(f"[POOLED] Added {len(all_chunks)} chunks to Qdrant collection '{settings.qdrant_collection}'")

    else:  # HYBRID
        threshold = settings.hybrid_threshold
        pooled_chunks = []
        for tenant, chunks in by_tenant.items():
            if len(chunks) >= threshold:
                path = faiss_save_for_tenant(tenant, chunks, emb)
                print(f"[HYBRID→SILOED] Tenant {tenant} ({len(chunks)} chunks) -> {path}")
            else:
                for c in chunks:
                    c.metadata["tenant_id"] = tenant
                pooled_chunks.extend(chunks)
                print(f"[HYBRID→POOLED] Tenant {tenant} ({len(chunks)} chunks) batched for pooled")
        if pooled_chunks:
            ensure_collection(emb)
            qdrant_pooled_add(pooled_chunks, emb)
            print(f"[HYBRID] Added {len(pooled_chunks)} pooled chunks to Qdrant")

if __name__ == "__main__":
    # Load the ingestion pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()
    run_ingestion(args.data_dir)
