import shutil
import tempfile
import uuid
from pathlib import Path
from fastapi import UploadFile

# All uploads for this PoC live under one temp directory, one subfolder per job
TEMP_DIR = Path(tempfile.gettempdir()) / "agentdesk_uploads"
TEMP_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def create_job_dir() -> tuple[str, Path]:
    """Creates a fresh, uniquely-named folder for one upload/run."""
    job_id = str(uuid.uuid4())
    job_dir = TEMP_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    return job_id, job_dir


def save_upload(upload_file: UploadFile, job_dir: Path) -> Path:
    """Streams the uploaded file to disk inside the job folder."""
    dest = job_dir / upload_file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return dest


def cleanup_job(job_dir: Path) -> None:
    """Removes a job's temp folder and everything in it."""
    shutil.rmtree(job_dir, ignore_errors=True)