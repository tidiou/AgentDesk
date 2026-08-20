import pandas as pd
import numpy as np

def _sanitize_for_json(obj):
    """
    Recursively converts numpy scalar types to native Python types,
    so the result is always safely JSON/Pydantic-serializable.
    Handles dicts, lists, and numpy scalars; leaves everything else as-is.
    """
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def compute_table_stats(df: pd.DataFrame) -> dict:
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

    if numeric_cols:
        stats["outliers"] = compute_outliers(df, numeric_cols)
        stats["trend_forecasts"] = compute_trend_forecast(df, numeric_cols)

    return _sanitize_for_json(stats)   # ← single point of safety, catches everything

# Outlier detection
def compute_outliers(df: pd.DataFrame, numeric_cols: list[str]) -> dict:
    outliers = {}
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue

        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flagged = series[(series < lower_bound) | (series > upper_bound)]

        if len(flagged) > 0:
            outliers[col] = {
                "count": int(len(flagged)),
                "percentage": round(float(len(flagged) / len(series) * 100), 1),
                "sample_values": [float(v) for v in flagged.head(5).tolist()],
                "normal_range": {
                    "lower": round(float(lower_bound), 2),
                    "upper": round(float(upper_bound), 2),
                },
            }
    return outliers

# Trend Forecast
def compute_trend_forecast(df: pd.DataFrame, numeric_cols: list[str], forecast_periods: int = 3) -> dict:
    """
    Fits a simple linear trend to each numeric column (using row order as
    a time proxy — assumes the data is chronologically ordered) and
    projects forward `forecast_periods` steps.
    """
    forecasts = {}
    x = np.arange(len(df))

    for col in numeric_cols:
        series = df[col]
        valid_mask = series.notna()
        if valid_mask.sum() < 3:
            continue  # need at least 3 points to fit a meaningful trend

        slope, intercept = np.polyfit(x[valid_mask], series[valid_mask], 1)

        if slope > 0.01:
            direction = "increasing"
        elif slope < -0.01:
            direction = "decreasing"
        else:
            direction = "stable"

        future_x = np.arange(len(df), len(df) + forecast_periods)
        forecast_values = (slope * future_x + intercept).round(2).tolist()

        forecasts[col] = {
            "direction": direction,
            "slope": round(float(slope), 4),
            "forecast_next_periods": forecast_values,
        }
    return forecasts





