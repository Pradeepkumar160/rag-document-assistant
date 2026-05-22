from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


def evaluate_rag(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
) -> Dict:
    """
    Run RAGAS evaluation on a list of Q&A pairs.

    Args:
        questions:     List of questions asked
        answers:       List of model-generated answers
        contexts:      List of context lists (retrieved chunks per question)
        ground_truths: List of reference answers

    Returns:
        Dictionary of RAGAS metric scores
    """
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }

    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )

    scores = result.to_pandas().to_dict(orient="records")
    logger.info(f"RAGAS evaluation complete: {scores}")
    return scores
