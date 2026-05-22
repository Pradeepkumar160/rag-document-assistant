from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, SourceDocument
from app.services.rag_pipeline import build_rag_chain
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def ask_question(request: ChatRequest):
    """
    Ask a question about the uploaded documents.
    Returns the answer and the source document chunks used.
    """
    try:
        chain = build_rag_chain()
        response = chain.invoke({"query": request.question})
    except Exception as e:
        logger.error(f"RAG chain error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer. Make sure a PDF is uploaded and Ollama is running. Error: {str(e)}"
        )

    sources = []
    for doc in response.get("source_documents", []):
        sources.append(
            SourceDocument(
                page_content=doc.page_content[:600],
                metadata=doc.metadata,
            )
        )

    return ChatResponse(
        question=request.question,
        answer=response.get("result", "No answer generated."),
        sources=sources,
    )
