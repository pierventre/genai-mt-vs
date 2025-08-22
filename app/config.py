from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    openai_api_key: str | None = None
    storage_mode: Literal["SILOED", "POOLED", "HYBRID"] = "HYBRID"
    hybrid_threshold: int = 100
    qdrant_collection: str = "documents"

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False

settings = Settings()
