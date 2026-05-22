from langchain_ollama import OllamaLLM
from app.core.config import settings


def get_llm() -> OllamaLLM:
    """Return a configured Ollama LLM instance."""
    return OllamaLLM(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0,
    )
