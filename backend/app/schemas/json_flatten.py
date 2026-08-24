from typing import Any
from pydantic import BaseModel


class FlattenedTable(BaseModel):
    table_name: str
    columns: list[str]
    row_count: int
    preview_rows: list[dict[str, Any]]
    all_rows: list[dict[str, Any]]


class JSONFlattenResponse(BaseModel):
    job_id: str
    source_filename: str
    tables: list[FlattenedTable]