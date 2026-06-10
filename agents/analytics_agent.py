import pandas as pd


def analytics_agent(state):

    df = state.get("data")

    if df is None:
        return {
            "analytics": {},
            "insights": "No dataset available"
        }

    if df.empty:
        return {
            "analytics": {
                "error": "No data returned"
            }
        }

    # ----------------------------
    # Detect numeric columns
    # ----------------------------

    numeric_cols = list(
        df.select_dtypes(include="number").columns
    )

    if not numeric_cols:
        return {
            "analytics": {
                "error": "No numeric columns found"
            }
        }

    # Use last numeric column as metric
    metric_col = numeric_cols[-1]

    # First non-metric column becomes dimension
    dimension_cols = [
        c for c in df.columns
        if c != metric_col
    ]

    dimension_col = (
        dimension_cols[0]
        if dimension_cols
        else metric_col
    )

    total = float(df[metric_col].sum())

    average = float(df[metric_col].mean())

    top_row = df.loc[
        df[metric_col].idxmax()
    ]

    bottom_row = df.loc[
        df[metric_col].idxmin()
    ]

    analytics = {
        "metric": metric_col,
        "dimension": dimension_col,
        "total": total,
        "average": average,
        "top_category": top_row[dimension_col],
        "top_value": float(top_row[metric_col]),
        "bottom_category": bottom_row[dimension_col],
        "bottom_value": float(bottom_row[metric_col]),
        "data": df.to_dict("records"),
        "data_type": "static_snapshot"
    }

    return {
        "analytics": analytics
    }