from fastapi import APIRouter, HTTPException
from app.models.schemas import EvaluationRequest, EvaluationResponse
from app.services.evaluator import evaluate_rag
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("/", response_model=EvaluationResponse)
def run_evaluation(request: EvaluationRequest):
    """
    Run RAGAS evaluation on provided Q&A pairs.
    Provide questions, model answers, retrieved contexts, and ground truth answers.
    """
    if not (len(request.questions) == len(request.answers) == len(request.contexts) == len(request.ground_truths)):
        raise HTTPException(
            status_code=400,
            detail="questions, answers, contexts, and ground_truths must all have the same length."
        )

    try:
        scores = evaluate_rag(
            questions=request.questions,
            answers=request.answers,
            contexts=request.contexts,
            ground_truths=request.ground_truths,
        )
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

    return EvaluationResponse(scores=scores)


@router.get("/demo", tags=["Evaluation"])
def run_demo_evaluation():
    """
    Run a quick demo evaluation with built-in sample data.
    """
    sample_questions = ["What is RAG?"]
    sample_answers = ["RAG stands for Retrieval-Augmented Generation, a framework that combines document retrieval with language model generation."]
    sample_contexts = [["Retrieval-Augmented Generation (RAG) is a framework that retrieves relevant documents and passes them to an LLM to generate grounded answers."]]
    sample_ground_truths = ["RAG is Retrieval-Augmented Generation — a method to ground LLM answers in retrieved documents."]

    try:
        scores = evaluate_rag(
            questions=sample_questions,
            answers=sample_answers,
            contexts=sample_contexts,
            ground_truths=sample_ground_truths,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo evaluation failed: {str(e)}")

    return EvaluationResponse(scores=scores, message="Demo evaluation complete")
