from pydantic import BaseModel
from typing import Literal


class ChartRecommendation(BaseModel):
    chart_type: Literal["bar", "line", "pie", "scatter"]
    title: str
    x_column: str
    y_column: str
    reason: str  # why this chart is useful, shown as a caption


class AnalyticsResponse(BaseModel):
    job_id: str
    source_filename: str
    summary: str                          # 2-3 sentence plain-language overview
    key_insights: list[str]               # bullet-point observations
    chart_recommendations: list[ChartRecommendation]
    raw_stats: dict                       # the computed pandas stats, for reference/debugging