def chart_agent(state):

    df = state.get("data")
    forecast = state.get("forecast_result")

    print("\n================ CHART AGENT ================")

    # =========================
    # CASE 1: FORECAST CHART
    # =========================
    if forecast is not None and not forecast.empty:

        cols = list(forecast.columns)

        # detect prophet output safely
        y_forecast_col = "yhat" if "yhat" in cols else cols[-1]

        return {
            "chart_type": "line_forecast",
            "chart_config": {
                "x": "ds",
                "y_actual": "y",
                "y_forecast": y_forecast_col,
                "title": "Actual vs Forecast"
            }
        }

    # =========================
    # CASE 2: NORMAL TIME SERIES
    # =========================
    if df is not None and not df.empty:

        cols = list(df.columns)

        if "ds" in cols:

            y_col = "y" if "y" in cols else df.select_dtypes(include="number").columns[-1]

            return {
                "chart_type": "line",
                "chart_config": {
                    "x": "ds",
                    "y": y_col,
                    "title": "Time Series Trend"
                }
            }

    # =========================
    # FALLBACK
    # =========================
    return {
        "chart_type": "table",
        "chart_config": {
            "title": "Raw Data View"
        }
    }