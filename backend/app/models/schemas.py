from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask about uploaded documents")


class SourceDocument(BaseModel):
    page_content: str
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceDocument]


class UploadResponse(BaseModel):
    message: str
    filename: str
    total_pages: int
    total_chunks: int


class EvaluationRequest(BaseModel):
    questions: List[str] = Field(..., description="Questions to evaluate")
    answers: List[str] = Field(..., description="Model-generated answers")
    contexts: List[List[str]] = Field(..., description="Retrieved context chunks per question")
    ground_truths: List[str] = Field(..., description="Reference answers")


class EvaluationResponse(BaseModel):
    scores: List[Dict[str, Any]]
    message: str = "Evaluation complete"
