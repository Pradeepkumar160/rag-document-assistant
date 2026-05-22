from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from app.services.pdf_loader import load_pdf
from app.services.chunker import split_documents
from app.core.vectordb import create_vectorstore
from app.core.config import settings
from app.models.schemas import UploadResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract text, chunk it, and store embeddings in ChromaDB.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Validate file size (max 50 MB)
    MAX_SIZE = 50 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum allowed size is 50 MB.")

    save_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    # Save file to disk
    with open(save_path, "wb") as buffer:
        buffer.write(contents)

    logger.info(f"Saved uploaded file to {save_path}")

    # Load, chunk, embed
    try:
        documents = load_pdf(save_path)
        chunks = split_documents(documents)
        create_vectorstore(chunks)
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return UploadResponse(
        message="PDF uploaded and indexed successfully.",
        filename=file.filename,
        total_pages=len(documents),
        total_chunks=len(chunks),
    )
