from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    CHROMA_DB_DIR: str = "chroma_db"
    UPLOAD_DIR: str = "uploads"
    LLM_MODEL: str = "llama3"
    EMBED_MODEL: str = "nomic-embed-text"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVER_K: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist at startup
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
