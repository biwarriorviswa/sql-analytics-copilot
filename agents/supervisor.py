
from agents.forecast_detector import forecast_detector


def route_query(question: str) -> dict:
    """
    Supervisor decides how the workflow should behave.
    Returns routing flags stored in state.
    """

    q = question.lower()

    config = {
        "run_forecast": False,
        "needs_approval": True,
        "chart_priority": "auto",
        "skip_analytics": False
    }

    # ----------------------------
    # Forecast detection
    # ----------------------------
    if forecast_detector(question):
        config["run_forecast"] = True

    # ----------------------------
    # Chart-heavy queries
    # ----------------------------
    chart_keywords = [
        "chart", "graph", "plot",
        "visualize", "trend"
    ]

    if any(k in q for k in chart_keywords):
        config["chart_priority"] = "visual"

    # ----------------------------
    # Risk-based approval logic
    # ----------------------------
    risky_keywords = [
        "delete", "drop", "truncate",
        "update", "insert", "alter"
    ]

    if any(k in q for k in risky_keywords):
        config["needs_approval"] = True
    else:
        # optional: auto-approve safe SELECT queries
        config["needs_approval"] = False

    return config