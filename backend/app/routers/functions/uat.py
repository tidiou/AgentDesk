from fastapi import APIRouter, HTTPException, Response
from app.functions.uat_export import build_uat_excel
from app.schemas.uat import UATGenerationResponse

from app.functions.uat_generator import generate_uat_spec
from app.schemas.uat import UATGenerationResponse
from app.services.job_store import get_job

router = APIRouter()


@router.post("/generate/{job_id}", response_model=UATGenerationResponse)
def generate_uat(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job found for id '{job_id}'")

    if job.category != "document":
        raise HTTPException(
            status_code=400,
            detail=f"UAT generation requires a document (pdf/docx/pptx/txt), got '{job.category}'",
        )

    try:
        result = generate_uat_spec(
            job_id=job_id,
            source_filename=job.parsed.filename,
            document_text=job.parsed.text,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UAT generation failed: {e}")

    return result

@router.post("/export")
def export_uat_excel(uat_result: UATGenerationResponse):
    buffer = build_uat_excel(uat_result.test_cases, uat_result.source_filename)

    filename = f"UAT_Spec_{uat_result.source_filename.rsplit('.', 1)[0]}.xlsx"

    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )