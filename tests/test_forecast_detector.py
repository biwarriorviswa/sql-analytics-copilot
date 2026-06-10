# tests/test_forecast_detector.py

from agents.forecast_detector import (
    needs_forecast
)


def test_forecast_keyword():

    question = (
        "Predict revenue for next month"
    )

    assert needs_forecast(question) is True


def test_forecast_keyword_future():

    question = (
        "What will sales be next quarter?"
    )

    assert needs_forecast(question) is True


def test_non_forecast_query():

    question = (
        "Show total sales by region"
    )

    assert needs_forecast(question) is False