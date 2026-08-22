import json
import pandas as pd


def flatten_json_to_dataframe(data) -> pd.DataFrame:
    """
    Flattens arbitrary JSON (a dict or a list of dicts) into a tabular
    DataFrame. Nested objects become dot-joined columns (e.g. address.city).
    Nested arrays are preserved as compact JSON strings within a cell,
    rather than being exploded into additional rows.
    """
    # Normalize to a list of records, since json_normalize expects that shape
    if isinstance(data, dict):
        records = [data]
    elif isinstance(data, list):
        records = data
    else:
        raise ValueError("JSON must be an object or an array of objects to flatten into a table")

    if not records:
        raise ValueError("JSON contains no data to flatten")

    df = pd.json_normalize(records, sep=".")

    # Any remaining cell that's still a list/dict (nested arrays json_normalize
    # couldn't flatten further) gets serialized to a compact JSON string,
    # so every cell ends up as a plain, table-safe value.
    for col in df.columns:
        df[col] = df[col].apply(
            lambda v: json.dumps(v, default=str) if isinstance(v, (list, dict)) else v
        )

    return df