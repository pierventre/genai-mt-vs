# genai-mt-vs

**genai-mt-vs** is a Python project for building and querying multi-tenant vector stores using three strategies: **SILOED**, **POOLED**, and **HYBRID**. It is designed for scalable, privacy-aware document search and retrieval in multi-tenant environments, such as SaaS platforms or enterprise applications.

---

## Features

- **Ingestion Pipeline:**  
  - Loads and preprocesses raw documents from a directory.
  - Chunks documents and annotates metadata (including PII flags).
  - Supports three storage strategies:
    - **SILOED:** Each tenant gets a private FAISS vector store.
    - **POOLED:** All tenants share a Qdrant collection, with tenant metadata.
    - **HYBRID:** Tenants with enough data get siloed stores; others are pooled.
  - Uses OpenAI embeddings (or configurable provider).

- **Query Demo:**  
  - Query the vector store for a given tenant and question.
  - Supports all three strategies, automatically falling back in HYBRID mode.
  - Prints top results with metadata for each tenant.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/genai-mt-vs.git
   cd genai-mt-vs
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure settings in `.env` or `config.py`:
   - `OPENAI_API_KEY`
   - `QDRANT_COLLECTION`
   - `STORAGE_MODE` (`SILOED`, `POOLED`, or `HYBRID`)
   - `HYBRID_THRESHOLD` (for hybrid mode)

---

## Usage

### 1. Ingest Documents

Run the ingestion pipeline to create vector stores:

```bash
python -m genai_mt_vs.ingestion --data-dir path/to/data
```

- `--data-dir`: Directory containing raw documents (default: `data`).

### 2. Query Vector Store

Run the demo query script:

```bash
python -m genai_mt_vs.query
```

- Queries for each tenant (e.g., `"tenantA"`, `"tenantB"`) using the `"HYBRID"` strategy.
- Prints top results and metadata.

---

## Storage Strategies

- **SILOED:**  
  Each tenant’s data is stored in a separate FAISS index for privacy and isolation.

- **POOLED:**  
  All tenants’ data is stored together in a Qdrant collection, with tenant IDs in metadata for filtering.

- **HYBRID:**  
  Tenants with enough data (above threshold) get siloed stores; others are pooled for efficiency.

---

## Project Structure

- `ingestion/`: Ingestion pipeline, chunking, embeddings, indexing.
- `query.py`: Query demo script.
- `config.py`: Configuration and settings.
- `connectors.py`, `preprocess.py`, `chunk.py`, `pii.py`, `embeddings.py`, `indexer.py`: Modular pipeline components.

---

## License

MIT

---

## Acknowledgements

- [FAISS](https://github.com/facebookresearch/faiss)
- [Qdrant](https://qdrant.tech/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
