from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping():
    return {"status": "analytics router is alive"}