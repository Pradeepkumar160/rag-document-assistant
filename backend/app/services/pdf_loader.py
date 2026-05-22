from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List
import logging

logger = logging.getLogger(__name__)


def load_pdf(file_path: str) -> List[Document]:
    """Load a PDF file and return a list of LangChain Document objects."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} pages from {file_path}")
    return documents
