from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.vectordb import load_vectorstore
from app.core.llm import get_llm
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Custom prompt to instruct the LLM to answer from context only
RAG_PROMPT_TEMPLATE = """You are a helpful document assistant. Use ONLY the following context to answer the question.
If the answer is not found in the context, say "I could not find the answer in the uploaded documents."

Context:
{context}

Question: {question}

Answer:"""

RAG_PROMPT = PromptTemplate(
    template=RAG_PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)


def build_rag_chain() -> RetrievalQA:
    """Build and return the RAG chain."""
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.RETRIEVER_K},
    )
    llm = get_llm()
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_PROMPT},
    )
    return chain
