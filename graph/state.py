from typing import TypedDict, Optional, Dict, Any
import pandas as pd


class WorkflowState(TypedDict, total=False):

    # =====================================================
    # User Input
    # =====================================================
    question: str
    user_query: str
    schema: str

    # =====================================================
    # SQL Pipeline
    # =====================================================
    generated_sql: str
    validated_sql: str
    optimized_sql: str

    validation: Dict[str, Any]

    # =====================================================
    # SQL Execution
    # =====================================================
    data: pd.DataFrame
    execution_error: str

    # =====================================================
    # Analytics
    # =====================================================
    analytics: Dict[str, Any]
    insights: str

    # =====================================================
    # Forecast Control
    # =====================================================
    run_forecast: bool
    forecast_horizon: Optional[int]
    forecast_granularity: Optional[str]

    forecast_result: Optional[pd.DataFrame]
    model_name: Optional[str]

    # =====================================================
    # Routing / Control
    # =====================================================
    needs_approval: bool
    approved: bool

    chart_priority: Optional[str]

    # =====================================================
    # Charts
    # =====================================================
    chart_type: Optional[str]
    chart_config: Dict[str, Any]

    # =====================================================
    # Final Output
    # =====================================================
    final_report: Dict[str, Any]