from pathlib import Path
import pandas as pd

from app.schemas.parsed import ParsedTable

PREVIEW_ROW_COUNT = 5


def _dataframe_to_parsed_table(df: pd.DataFrame, filepath: Path, file_type: str) -> ParsedTable:
    # Pydantic needs plain Python types — pandas objects (NaN, Timestamp, int64, etc.)
    # aren't natively JSON-serializable, so we convert the preview rows explicitly.
    preview_df = df.head(PREVIEW_ROW_COUNT)
    preview_rows = preview_df.where(pd.notnull(preview_df), None).to_dict(orient="records")

    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    return ParsedTable(
        filename=filepath.name,
        file_type=file_type,
        columns=list(df.columns),
        row_count=len(df),
        preview_rows=preview_rows,
        dtypes=dtypes,
    )


def parse_csv(filepath: Path) -> ParsedTable:
    try:
        df = pd.read_csv(filepath)
    except UnicodeDecodeError:
        # Fallback for files not saved as UTF-8 (common with Excel exports)
        df = pd.read_csv(filepath, encoding="latin-1")

    if df.empty:
        raise ValueError(f"'{filepath.name}' contains no data")

    return _dataframe_to_parsed_table(df, filepath, "csv")


def parse_excel(filepath: Path) -> ParsedTable:
    ext = filepath.suffix.lower()
    file_type = "xlsx" if ext == ".xlsx" else "xls"

    # Multi-sheet handling deferred (per earlier decision) — grab the first sheet only for now
    df = pd.read_excel(filepath, sheet_name=0)

    if df.empty:
        raise ValueError(f"'{filepath.name}' contains no data")

    return _dataframe_to_parsed_table(df, filepath, file_type)


def parse_table(filepath: Path) -> ParsedTable:
    """Dispatches to the correct parser based on file extension."""
    ext = filepath.suffix.lower()
    if ext == ".csv":
        return parse_csv(filepath)
    elif ext in (".xlsx", ".xls"):
        return parse_excel(filepath)
    else:
        raise ValueError(f"'{ext}' is not a supported table type")