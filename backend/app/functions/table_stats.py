import pandas as pd


def compute_table_stats(df: pd.DataFrame) -> dict:
    """
    Deterministically computes summary statistics from a dataframe.
    This is the 'ground truth' the AI will reason over — no AI involved here.
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    stats = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": {},
        "categorical_summary": {},
    }

    for col in numeric_cols:
        stats["numeric_summary"][col] = {
            "mean": round(df[col].mean(), 2),
            "min": df[col].min(),
            "max": df[col].max(),
            "std_dev": round(df[col].std(), 2),
        }

    for col in categorical_cols:
        top_values = df[col].value_counts().head(5).to_dict()
        stats["categorical_summary"][col] = {
            "unique_count": df[col].nunique(),
            "top_values": top_values,
        }

    if len(numeric_cols) >= 2:
        stats["correlations"] = df[numeric_cols].corr().round(2).to_dict()

    return stats