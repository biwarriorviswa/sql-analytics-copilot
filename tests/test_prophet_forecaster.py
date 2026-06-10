# tests/test_prophet_forecaster.py

import pandas as pd

from forecasting.prophet_forecaster import (
    ProphetForecaster
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


def test_prophet_forecast():

    forecaster = ProphetForecaster()

    forecast = forecaster.forecast(
        df=sample_data(),
        date_col="date",
        value_col="sales",
        periods=30
    )

    assert forecast is not None

    assert "yhat" in forecast.columns

    assert len(forecast) >= 130