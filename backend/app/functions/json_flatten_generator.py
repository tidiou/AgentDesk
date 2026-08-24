from app.functions.json_flatten import detect_flattenable_tables
from app.schemas.json_flatten import JSONFlattenResponse, FlattenedTable
from app.services.ai_client import call_ai_tool

PREVIEW_ROW_COUNT = 20

SYSTEM_PROMPT = """You are helping curate flattened data tables for a business \
user. You will be given, for each table, the full list of available columns \
(from fully flattening nested JSON) and a sample row.

For each table, select the subset of columns that a business user would \
actually want to see — identifying fields, key attributes, and the most \
useful summary values. Prefer scalar, human-readable fields over verbose or \
rarely-needed detail (e.g. prefer a single 'address.city' over every address \
sub-field; prefer one key performance metric over an entire nested breakdown \
unless several are genuinely all useful). Every selected column name must be \
copied exactly from the provided list — do not invent or rename columns."""

TABLE_SELECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "table_selections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"},
                    "selected_columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Column names to keep, copied exactly from the provided available_columns list",
                    },
                },
                "required": ["table_name", "selected_columns"],
            },
        },
    },
    "required": ["table_selections"],
}


def generate_json_flatten(job_id: str, source_filename: str, data) -> JSONFlattenResponse:
    raw_tables = detect_flattenable_tables(data)

    # Build the AI's input: table name, available columns, one sample row per table
    tables_summary = []
    for name, df in raw_tables.items():
        sample_row = df.where(df.notnull(), None).iloc[0].to_dict()
        tables_summary.append({
            "table_name": name,
            "available_columns": list(df.columns),
            "sample_row": sample_row,
        })

    user_message = f"Here are the tables to curate:\n\n{tables_summary}"

    result = call_ai_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="select_table_columns",
        tool_description="Select the most relevant columns for each table",
        input_schema=TABLE_SELECTION_SCHEMA,
        max_tokens=2048,
    )

    selections = {sel["table_name"]: sel["selected_columns"] for sel in result["table_selections"]}

    final_tables = []
    for name, df in raw_tables.items():
        chosen_columns = [c for c in selections.get(name, []) if c in df.columns]
        if not chosen_columns:
            chosen_columns = list(df.columns)  # fallback: AI gave nothing usable, keep everything

        curated_df = df[chosen_columns].where(df[chosen_columns].notnull(), None)
        all_rows = curated_df.to_dict(orient="records")

        final_tables.append(FlattenedTable(
            table_name=name,
            columns=chosen_columns,
            row_count=len(curated_df),
            preview_rows=all_rows[:PREVIEW_ROW_COUNT],
            all_rows=all_rows,
        ))

    return JSONFlattenResponse(job_id=job_id, source_filename=source_filename, tables=final_tables)