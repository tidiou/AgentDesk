import pandas as pd
from fastapi import APIRouter, HTTPException

from app.functions.analytics_generator import generate_analytics
from app.schemas.analytics import AnalyticsResponse
from app.services.job_store import get_job

router = APIRouter()


def _load_dataframe(filepath, file_type: str) -> pd.DataFrame:
    """Re-reads the stored file into a dataframe for analysis."""
    if file_type == "csv":
        return pd.read_csv(filepath)
    elif file_type in ("xlsx", "xls"):
        return pd.read_excel(filepath, sheet_name=0)
    else:
        raise ValueError(f"Cannot load '{file_type}' as a dataframe")


@router.post("/generate/{job_id}", response_model=AnalyticsResponse)
def generate_table_analytics(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job found for id '{job_id}'")

    if job.category != "table":
        raise HTTPException(
            status_code=400,
            detail=f"Analytics requires a table (csv/xlsx/xls), got '{job.category}'",
        )

    try:
        df = _load_dataframe(job.filepath, job.parsed.file_type)
        result = generate_analytics(
            job_id=job_id,
            source_filename=job.parsed.filename,
            df=df,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics generation failed: {e}")

    return result