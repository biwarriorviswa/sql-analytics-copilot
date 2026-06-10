import streamlit as st
import pandas as pd

from graph.workflow import build_workflow
from dashboard.reports import render_report
from dashboard.charts import render_chart

workflow = build_workflow()

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="SQL Analytics Copilot",
    layout="wide"
)

st.title("SQL Analytics Copilot")

# =========================
# HELPER
# =========================
def make_arrow_safe(df):
    """
    Prevent Streamlit Arrow serialization errors
    with datetime/object columns.
    """
    if df is None:
        return None

    df = df.copy()

    for col in df.columns:
        try:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)

            elif df[col].dtype == "object":
                if len(df) > 0 and hasattr(df[col].iloc[0], "strftime"):
                    df[col] = df[col].astype(str)

        except Exception:
            pass

    return df


query = st.text_area("Ask a business question")

if st.button("Run"):

    # =========================
    # VALIDATION
    # =========================
    if not query.strip():
        st.warning("Please enter a question")
        st.stop()

    state = {
        "question": query,
        "run_forecast": False,
        "needs_approval": True,
        "approved": True
    }

    # =========================
    # RUN WORKFLOW
    # =========================
    result = workflow.invoke(state)

    # =========================
    # REPORT
    # =========================
    render_report(result)

    # =========================
    # DATA
    # =========================
    df = result.get("data")
    forecast_df = result.get("forecast_result")

    if df is not None:
        df = make_arrow_safe(df)

    if forecast_df is not None:
        forecast_df = make_arrow_safe(forecast_df)

    # =========================
    # RAW DATA
    # =========================
    if df is not None and not df.empty:
        st.subheader("📊 Query Result")
        st.dataframe(df)

    # =========================
    # FORECAST TABLE
    # =========================
    if forecast_df is not None and not forecast_df.empty:
        st.subheader("📈 Forecast Result")
        st.dataframe(forecast_df)

    # =========================
    # CHART CONFIG
    # =========================
    chart_type = result.get("chart_type")
    chart_config = result.get("chart_config")

    # =========================
    # FORECAST CHART
    # =========================
    if (
        chart_type == "line_forecast"
        and df is not None
        and forecast_df is not None
        and not df.empty
        and not forecast_df.empty
    ):

        st.subheader("📈 Actual vs Forecast")

        try:
            actual = df[["ds", "y"]].copy()
            actual["type"] = "Actual"

            forecast = forecast_df[["ds", "yhat"]].copy()
            forecast = forecast.rename(columns={"yhat": "y"})
            forecast["type"] = "Forecast"

            combined = pd.concat(
                [actual, forecast],
                ignore_index=True
            )

            render_chart(
                combined,
                {
                    "chart_type": "line",
                    "config": {
                        "x": "ds",
                        "y": "y",
                        "color": "type",
                        "title": "Actual vs Forecast"
                    }
                }
            )

        except Exception as e:
            st.error(f"Forecast chart failed: {e}")
            st.dataframe(combined)

    # =========================
    # NORMAL CHART
    # =========================
    elif chart_config and df is not None and not df.empty:

        st.subheader("📊 Visualization")

        try:
            render_chart(
                df,
                {
                    "chart_type": chart_type,
                    "config": chart_config
                }
            )

        except Exception as e:
            st.error(f"Chart rendering failed: {e}")

    # =========================
    # FALLBACK
    # =========================
    elif df is not None and not df.empty:

        st.subheader("📊 Data View")
        st.dataframe(df)

    # =========================
    # DEBUG SECTION
    # =========================
    with st.expander("Debug"):

        st.write("Chart Type:", chart_type)
        st.write("Chart Config:", chart_config)

        st.write("Forecast Available:",
                 forecast_df is not None)

        if forecast_df is not None:
            st.write("Forecast Shape:",
                     forecast_df.shape)