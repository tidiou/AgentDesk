from typing import Any
from pydantic import BaseModel


class JSONFlattenResponse(BaseModel):
    job_id: str
    source_filename: str
    columns: list[str]
    row_count: int
    preview_rows: list[dict[str, Any]]   # capped, for on-screen display
    all_rows: list[dict[str, Any]]        # full data, used for Excel export