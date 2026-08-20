import json
import pandas as pd

from app.functions.table_stats import compute_table_stats
from app.schemas.analytics import AnalyticsResponse, ChartRecommendation
from app.services.ai_client import call_ai_tool

SYSTEM_PROMPT = """You are a data analyst. You will be given summary statistics \
computed from a dataset (not the raw data itself) — column names, types, means, \
distributions, missing values, correlations, detected outliers, and simple linear \
trend forecasts where available.

Your job is to:
1. Write a brief plain-language summary of what this dataset appears to represent
2. Identify specific, genuinely interesting insights — trends, imbalances, outliers, \
data quality concerns (e.g. high missing-value counts), or notable correlations. \
If outliers were detected, explicitly call out which columns and how significant \
they are. If a trend forecast shows a meaningful increasing or decreasing \
direction, mention what that implies going forward.
3. Recommend 2-4 charts that would best help a business user understand this data. \
Only recommend charts using column names that actually exist in the dataset. \
Prefer bar charts for categorical comparisons, line charts for trends over an \
ordered/time-like column (especially where a trend forecast exists), pie charts \
only for a column with a small number of categories, and a scatter chart \
specifically when a column has detected outliers — use the y_column to name \
the column that has outliers."""

ANALYTICS_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "A 2-3 sentence plain-language overview of what this dataset contains and its overall shape",
        },
        "key_insights": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Specific, notable observations about the data — trends, outliers, imbalances, data quality issues",
        },
        "chart_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "chart_type": {"type": "string", "enum": ["bar", "line", "pie", "scatter"]},
                    "title": {"type": "string"},
                    "x_column": {"type": "string", "description": "Must be an actual column name from the dataset"},
                    "y_column": {"type": "string", "description": "Must be an actual column name from the dataset"},
                    "reason": {"type": "string"},
                },
                "required": ["chart_type", "title", "x_column", "y_column", "reason"],
            },
            "description": "2-4 chart suggestions...",
        },
    },
    "required": ["summary", "key_insights", "chart_recommendations"],
}


def generate_analytics(job_id: str, source_filename: str, df: pd.DataFrame) -> AnalyticsResponse:
    stats = compute_table_stats(df)

    user_message = (
        f"Here are the computed statistics for the dataset '{source_filename}':\n\n"
        f"{json.dumps(stats, indent=2, default=str)}"
    )

    result = call_ai_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="generate_data_analytics",
        tool_description="Generate insights and chart recommendations from dataset statistics",
        input_schema=ANALYTICS_TOOL_SCHEMA,
        max_tokens=4096,
    )

    chart_recommendations = [ChartRecommendation(**c) for c in result["chart_recommendations"]]

    return AnalyticsResponse(
        job_id=job_id,
        source_filename=source_filename,
        summary=result["summary"],
        key_insights=result["key_insights"],
        chart_recommendations=chart_recommendations,
        raw_stats=stats,
    )