from langchain_ollama import OllamaEmbeddings
from app.core.config import settings


def get_embedding_model() -> OllamaEmbeddings:
    """Return a configured Ollama embedding model instance."""
    return OllamaEmbeddings(
        model=settings.EMBED_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )
