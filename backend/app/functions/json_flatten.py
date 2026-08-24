import json
import pandas as pd




def detect_flattenable_tables(data) -> dict[str, pd.DataFrame]:
    """
    Scans JSON for array-of-objects fields and flattens each into its own
    table. Handles two top-level shapes:
    - A JSON object with one or more array-of-objects fields (each becomes
      a named table, e.g. {"employees": [...], "projects": [...]})
    - A bare top-level array of objects (becomes a single table named "data")
    """
    if isinstance(data, list):
        if not data or not all(isinstance(item, dict) for item in data):
            raise ValueError("Top-level array must contain objects to flatten into a table")
        df = pd.json_normalize(data, sep=".")
        for col in df.columns:
            df[col] = df[col].apply(
                lambda v: json.dumps(v, default=str) if isinstance(v, (list, dict)) else v
            )
        return {"data": df}

    if not isinstance(data, dict):
        raise ValueError("JSON must be an object or an array of objects to flatten into a table")

    tables = {}
    for key, value in data.items():
        if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            df = pd.json_normalize(value, sep=".")
            for col in df.columns:
                df[col] = df[col].apply(
                    lambda v: json.dumps(v, default=str) if isinstance(v, (list, dict)) else v
                )
            tables[key] = df

    if not tables:
        raise ValueError("No array-of-objects fields found to flatten into tables")

    return tables