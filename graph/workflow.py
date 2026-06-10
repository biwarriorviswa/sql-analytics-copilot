from langgraph.graph import StateGraph, END

from graph.state import WorkflowState
from database.schema_loader import load_schema
from database.mysql import execute_sql

from agents.sql_agent import sql_agent
from agents.validator import validator
from agents.optimizer import optimizer

from agents.analytics_agent import analytics_agent
from agents.insight_agent import insight_agent

from agents.forecast_detector import forecast_detector
from agents.forecast_agent import forecast_agent
from agents.chart_agent import chart_agent


# =========================
# DEBUG HELPER
# =========================
def debug_state(node_name, state):
    print(f"\n========== DEBUG [{node_name}] ==========")
    print("question:", state.get("question"))
    print("run_forecast:", state.get("run_forecast"))
    print("generated_sql:", state.get("generated_sql"))
    print("optimized_sql:", state.get("optimized_sql"))
    print("validation:", state.get("validation"))

    if state.get("data") is not None:
        print("data_shape:", getattr(state["data"], "shape", None))

    print("forecast_result:", state.get("forecast_result"))
    print("forecast_error:", state.get("forecast_error"))

    print("chart_type:", state.get("chart_type"))
    print("chart_config:", state.get("chart_config"))

    print("keys:", list(state.keys()))


# =========================
# SUPERVISOR
# =========================
def supervisor_node(state):

    state["schema"] = state.get("schema") or load_schema()
    state["user_query"] = state.get("question")

    print("\n================ SUPERVISOR ================")
    print("USER QUERY:", state["user_query"])

    result = forecast_detector(state)

    state["run_forecast"] = result.get("run_forecast", False)
    state.update(result)

    debug_state("SUPERVISOR", state)
    return state


# =========================
# SQL NODE
# =========================
def sql_node(state):

    print("\n================ SQL AGENT ================")
    result = sql_agent(state)

    state.update(result)
    debug_state("SQL AGENT", state)
    return state


# =========================
# VALIDATOR
# =========================
def validator_node(state):

    print("\n================ VALIDATOR ================")
    result = validator(state)

    state.update(result)
    debug_state("VALIDATOR", state)
    return state


# =========================
# OPTIMIZER
# =========================
def optimizer_node(state):

    print("\n================ OPTIMIZER ================")
    result = optimizer(state)

    state.update(result)
    debug_state("OPTIMIZER", state)
    return state


# =========================
# EXECUTE
# =========================
def execute_node(state):

    sql = state.get("optimized_sql") or state.get("generated_sql")

    print("\n================ EXECUTE ================")
    print("FINAL SQL:", sql)

    if not sql:
        state["data"] = None
        state["execution_error"] = "Missing SQL"
        return state

    try:
        df = execute_sql(sql)

        print("ROWS:", len(df))
        print(df.head())

        state["data"] = df
        state["execution_error"] = None

    except Exception as e:
        state["data"] = None
        state["execution_error"] = str(e)
        print("ERROR:", e)

    debug_state("EXECUTE", state)
    return state


# =========================
# ANALYTICS
# =========================
def analytics_node(state):

    print("\n================ ANALYTICS ================")

    if state.get("data") is None:
        state["analytics"] = {}
        return state

    result = analytics_agent(state)
    state.update(result)

    debug_state("ANALYTICS", state)
    return state


# =========================
# INSIGHTS
# =========================
def insight_node(state):

    print("\n================ INSIGHTS ================")

    result = insight_agent(state)
    state.update(result)

    debug_state("INSIGHTS", state)
    return state


# =========================
# FORECAST
# =========================
def forecast_node(state):

    print("\n================ FORECAST ================")

    state["model_name"] = "prophet"
    state["forecast_horizon"] = state.get("forecast_horizon", 6)

    result = forecast_agent(state)

    state["forecast_result"] = result.get("forecast_result")
    state["forecast_error"] = result.get("forecast_error")

    print("FORECAST RESULT:", state["forecast_result"] is not None)
    print("FORECAST ERROR:", state["forecast_error"])

    debug_state("FORECAST", state)
    return state


# =========================
# CHART NODE (FINAL FIXED)
# =========================
def chart_node(state):

    print("\n================ CHART NODE ================")

    result = chart_agent(state)

    state.update(result)

    print("CHART TYPE:", state.get("chart_type"))
    print("CHART CONFIG:", state.get("chart_config"))

    debug_state("CHART", state)
    return state


# =========================
# ROUTING
# =========================
def route_after_validator(state):

    if state.get("validation", {}).get("valid"):
        return "optimizer"

    print("❌ VALIDATION FAILED")
    return END


def route_after_insights(state):

    if state.get("run_forecast"):
        return "forecast"

    # always go to chart if no forecast
    return "chart"


# =========================
# BUILD WORKFLOW
# =========================
def build_workflow():

    workflow = StateGraph(WorkflowState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("sql", sql_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("optimizer", optimizer_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("insights", insight_node)

    workflow.add_node("forecast", forecast_node)
    workflow.add_node("chart", chart_node)

    workflow.set_entry_point("supervisor")

    workflow.add_edge("supervisor", "sql")
    workflow.add_edge("sql", "validator")

    workflow.add_conditional_edges(
        "validator",
        route_after_validator,
        {
            "optimizer": "optimizer",
            END: END
        }
    )

    workflow.add_edge("optimizer", "execute")
    workflow.add_edge("execute", "analytics")
    workflow.add_edge("analytics", "insights")

    workflow.add_conditional_edges(
        "insights",
        route_after_insights,
        {
            "forecast": "forecast",
            "chart": "chart"
        }
    )

    workflow.add_edge("forecast", "chart")  # 🔥 CRITICAL FIX
    workflow.add_edge("chart", END)

    return workflow.compile()