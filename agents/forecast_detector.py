# agents/forecast_detector.py

FORECAST_KEYWORDS = [
    "forecast",
    "predict",
    "prediction",
    "future",
    "next",
    "projection",
    "estimate",
    "trend"
]


def forecast_detector(state_or_query):
    """
    Supports both:
    - forecast_detector(state)
    - forecast_detector(str)
    """

    # =========================
    # Extract question safely
    # =========================
    if isinstance(state_or_query, dict):
        question = state_or_query.get("user_query") or state_or_query.get("question") or ""
        state = state_or_query
    else:
        question = str(state_or_query)
        state = {}

    question_lower = question.lower()

    # =========================
    # Detect forecast intent
    # =========================
    is_forecast = any(
        keyword in question_lower
        for keyword in FORECAST_KEYWORDS
    )

    print("\n========== FORECAST DETECTOR ==========")
    print("QUESTION:", question)
    print("DETECTED:", is_forecast)

    # =========================
    # RETURN CONSISTENT STATE KEY
    # =========================
    return {
        **state,
        "run_forecast": is_forecast
    }