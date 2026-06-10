# agents/forecast_agent.py

import pandas as pd
from forecasting.model_registry import ModelRegistry


def forecast_agent(state):
    """
    Clean + stable forecasting agent
    Compatible with LangGraph workflow + Streamlit UI
    """

    # =========================
    # SAFE FLAG CHECK
    # =========================
    if not state.get("run_forecast", False):
        return {
            "forecast_result": None,
            "forecast_error": None
        }

    df = state.get("data")

    if df is None or df.empty:
        return {
            "forecast_result": None,
            "forecast_error": "Empty dataset"
        }

    model_name = state.get("model_name", "prophet")
    periods = state.get("forecast_horizon", 6)

    df = df.copy()

    # =========================
    # COLUMN DETECTION (ROBUST)
    # =========================
    date_col = state.get("date_col")
    value_col = state.get("value_col")

    if not date_col:
        if "ds" in df.columns:
            date_col = "ds"
        else:
            date_col = df.columns[0]

    if not value_col:
        if "y" in df.columns:
            value_col = "y"
        else:
            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) == 0:
                return {
                    "forecast_result": None,
                    "forecast_error": "No numeric column found"
                }

            value_col = numeric_cols[-1]

    # =========================
    # CLEAN DATA
    # =========================
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    df = df.dropna(subset=[date_col, value_col])

    if df.empty:
        return {
            "forecast_result": None,
            "forecast_error": "No valid rows after cleaning"
        }

    # =========================
    # NORMALIZE TIME SERIES
    # =========================
    df[date_col] = df[date_col].dt.to_period("M").dt.to_timestamp()

    df = df.groupby(date_col, as_index=False)[value_col].sum()
    df = df.sort_values(date_col)

    # =========================
    # VALIDATION
    # =========================
    if len(df) < 3:
        return {
            "forecast_result": None,
            "forecast_error": "Need at least 3 time periods"
        }

    if df[value_col].nunique() <= 1:
        return {
            "forecast_result": None,
            "forecast_error": "Flat time series detected"
        }

    # =========================
    # FORECAST MODEL
    # =========================
    try:
        model = ModelRegistry.get_model(model_name)

        forecast = model.forecast(
            df=df,
            date_col=date_col,
            value_col=value_col,
            periods=periods
        )

        # 🔥 IMPORTANT: ensure output is DataFrame
        if not isinstance(forecast, pd.DataFrame):
            forecast = pd.DataFrame(forecast)

        return {
            "forecast_result": forecast,
            "forecast_error": None,
            "model_name": model_name,
            "date_col": date_col,
            "value_col": value_col
        }

    except Exception as e:
        return {
            "forecast_result": None,
            "forecast_error": f"Forecast failed: {str(e)}"
        }