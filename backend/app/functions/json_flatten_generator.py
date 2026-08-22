from app.functions.json_flatten import flatten_json_to_dataframe
from app.schemas.json_flatten import JSONFlattenResponse

PREVIEW_ROW_COUNT = 20


def generate_json_flatten(job_id: str, source_filename: str, data) -> JSONFlattenResponse:
    df = flatten_json_to_dataframe(data)

    # NaN isn't JSON-safe, same fix pattern as table_parser.py
    safe_df = df.where(df.notnull(), None)

    all_rows = safe_df.to_dict(orient="records")

    return JSONFlattenResponse(
        job_id=job_id,
        source_filename=source_filename,
        columns=list(df.columns),
        row_count=len(df),
        preview_rows=all_rows[:PREVIEW_ROW_COUNT],
        all_rows=all_rows,
    )