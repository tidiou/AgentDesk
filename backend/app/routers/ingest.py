from fastapi import APIRouter, UploadFile, File, HTTPException

from app.parsers import parse_any
from app.parsers.base import get_file_category, UnsupportedFileTypeError
from app.schemas.requests import IngestResponse
from app.services.job_store import save_job, delete_job, JobRecord
from app.services.file_storage import (
    create_job_dir,
    save_upload,
    cleanup_job,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
)

router = APIRouter()


@router.post("/upload", response_model=IngestResponse)
async def upload_file(file: UploadFile = File(...)):
    # Guard 1: size limit — checked before we even save to disk, where possible
    if file.size is not None and file.size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"'{file.filename}' exceeds the {MAX_FILE_SIZE_MB}MB size limit",
        )

    # Guard 2: unsupported extension — fail fast before touching disk
    try:
        category = get_file_category(file.filename)
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job_id, job_dir = create_job_dir()
    filepath = save_upload(file, job_dir)

    try:
        parsed = parse_any(filepath)
    except ValueError as e:
        cleanup_job(job_dir)
        delete_job(job_id)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {e}")

    save_job(job_id, JobRecord(
        job_dir=job_dir,
        filepath=filepath,
        category=category,
        parsed=parsed,
    ))

    return IngestResponse(job_id=job_id, category=category, parsed=parsed)