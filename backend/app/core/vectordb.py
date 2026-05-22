from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List
from app.core.embeddings import get_embedding_model
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def create_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Create (or add to) a persistent Chroma vector store.
    Using collection_name so multiple uploads accumulate in the same DB.
    """
    embedding_model = get_embedding_model()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name="rag_docs",
    )
    logger.info(f"Stored {len(chunks)} chunks into ChromaDB.")
    return vectordb


def load_vectorstore() -> Chroma:
    """Load an existing Chroma vector store from disk."""
    embedding_model = get_embedding_model()
    vectordb = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embedding_model,
        collection_name="rag_docs",
    )
    return vectordb
