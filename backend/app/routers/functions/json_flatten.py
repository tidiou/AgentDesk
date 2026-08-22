from io import BytesIO
import pandas as pd
from fastapi import APIRouter, HTTPException, Response

from app.functions.json_flatten_generator import generate_json_flatten
from app.schemas.json_flatten import JSONFlattenResponse
from app.services.job_store import get_job

router = APIRouter()


@router.post("/generate/{job_id}", response_model=JSONFlattenResponse)
def generate_flattened_table(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job found for id '{job_id}'")

    if job.category != "structured":
        raise HTTPException(
            status_code=400,
            detail=f"Flattening requires a JSON file, got '{job.category}'",
        )

    try:
        result = generate_json_flatten(
            job_id=job_id,
            source_filename=job.parsed.filename,
            data=job.parsed.data,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flattening failed: {e}")

    return result


@router.post("/export")
def export_flattened_excel(result: JSONFlattenResponse):
    df = pd.DataFrame(result.all_rows, columns=result.columns)

    buffer = BytesIO()
    df.to_excel(buffer, index=False, sheet_name="Flattened Data")
    buffer.seek(0)

    filename = f"Flattened_{result.source_filename.rsplit('.', 1)[0]}.xlsx"

    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )