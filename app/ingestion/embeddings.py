import hashlib
import numpy as np
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings

class MockEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._fake_vector(t) for t in texts]
    def embed_query(self, text: str) -> List[float]:
        return self._fake_vector(text)
    def _fake_vector(self, text: str) -> List[float]:
        np.random.seed(int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32))
        return np.random.rand(384).tolist()

class EmbeddingProvider:
    def __init__(self, api_key: str | None):
        self.cache = {}
        self.impl = OpenAIEmbeddings(api_key=api_key) if api_key else MockEmbeddings()

    def embed_text(self, text: str) -> list[float]:
        h = hashlib.md5(text.encode()).hexdigest()
        if h in self.cache:
            return self.cache[h]
        v = self.impl.embed_query(text)
        self.cache[h] = v
        return v

    def embedding_fn(self):
        # LangChain vectorstores accept an Embeddings object, not a function
        return self.impl
