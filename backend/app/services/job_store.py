from pathlib import Path
from dataclasses import dataclass
from typing import Literal, Union

from app.schemas.parsed import ParsedDocument, ParsedTable, ParsedStructured

ParsedResult = Union[ParsedDocument, ParsedTable, ParsedStructured]


@dataclass
class JobRecord:
    job_dir: Path
    filepath: Path
    category: Literal["document", "table", "structured"]
    parsed: ParsedResult


# Process-wide in-memory store. Lost on restart — acceptable for the PoC's
# no-persistence scope. If this ever needs to survive restarts or scale
# beyond one process, this is the piece that gets swapped for Redis/a DB.
_jobs: dict[str, JobRecord] = {}


def save_job(job_id: str, record: JobRecord) -> None:
    _jobs[job_id] = record


def get_job(job_id: str) -> JobRecord | None:
    return _jobs.get(job_id)


def delete_job(job_id: str) -> None:
    _jobs.pop(job_id, None)