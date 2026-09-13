from typing import Literal, Union
from pydantic import BaseModel

from app.schemas.parsed import ParsedDocument, ParsedTable, ParsedStructured, ParsedPcap


class IngestResponse(BaseModel):
    job_id: str
    category: Literal["document", "table", "structured", "network"]
    parsed: Union[ParsedDocument, ParsedTable, ParsedStructured, ParsedPcap]