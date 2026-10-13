from fastapi import APIRouter, HTTPException

from app.functions.summary_generator import generate_summary
from app.schemas.summary import DocumentSummaryResponse
from app.services.job_store import get_job
from app.services.ai_client import OutputTruncatedError

router = APIRouter()


@router.post("/generate/{job_id}", response_model=DocumentSummaryResponse)
def generate_document_summary(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job found for id '{job_id}'")

    if job.category != "document":
        raise HTTPException(
            status_code=400,
            detail=f"Summarization requires a document (pdf/docx/pptx/txt), got '{job.category}'",
        )

    try:
        result = generate_summary(
            job_id=job_id,
            source_filename=job.parsed.filename,
            document_text=job.parsed.text,
        )
    except OutputTruncatedError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    return result