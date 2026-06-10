# tests/test_forecast_agent.py

import pandas as pd

from agents.forecast_agent import (
    ForecastAgent
)


class MockModel:

    def forecast(
        self,
        df,
        date_col,
        value_col,
        periods
    ):

        return pd.DataFrame({
            "forecast": [100, 120]
        })


def test_forecast_agent(monkeypatch):

    from forecasting.model_registry import (
        ModelRegistry
    )

    monkeypatch.setattr(
        ModelRegistry,
        "get_model",
        lambda x: MockModel()
    )

    df = pd.DataFrame({
        "date": pd.date_range(
            start="2024-01-01",
            periods=10
        ),
        "sales": range(10)
    })

    agent = ForecastAgent()

    result = agent.run(
        df=df,
        forecast_required=True,
        date_col="date",
        value_col="sales",
        model_name="prophet"
    )

    assert result is not None

    assert "forecast" in result.columns


def test_forecast_not_required():

    agent = ForecastAgent()

    result = agent.run(
        df=None,
        forecast_required=False
    )

    assert result is None