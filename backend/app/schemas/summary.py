from pydantic import BaseModel


class DocumentSummaryResponse(BaseModel):
    job_id: str
    source_filename: str
    salient_points: list[str]      # the key facts/ideas, distilled
    red_thread: str | None          # the connecting theme/narrative, if one exists
    takeaways: list[str]            # actionable or notable conclusions