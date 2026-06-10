# tests/test_xgboost_forecaster.py

import pandas as pd

from forecasting.xgboost_forecaster import (
    XGBoostForecaster
)


def sample_data():

    return pd.DataFrame({
        "date": pd.date_range(
            start="2024-01-01",
            periods=100,
            freq="D"
        ),
        "sales": range(100)
    })


def test_xgboost_forecast():

    forecaster = XGBoostForecaster()

    forecast = forecaster.forecast(
        df=sample_data(),
        date_col="date",
        value_col="sales",
        periods=30
    )

    assert forecast is not None

    assert len(forecast) == 30

    assert "forecast" in forecast.columns