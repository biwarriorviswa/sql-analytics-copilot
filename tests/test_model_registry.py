# tests/test_model_registry.py

import pytest

from forecasting.model_registry import ModelRegistry
from forecasting.prophet_forecaster import ProphetForecaster
from forecasting.xgboost_forecaster import XGBoostForecaster


def test_get_prophet_model():

    model = ModelRegistry.get_model("prophet")

    assert isinstance(
        model,
        ProphetForecaster
    )


def test_get_xgboost_model():

    model = ModelRegistry.get_model("xgboost")

    assert isinstance(
        model,
        XGBoostForecaster
    )


def test_invalid_model():

    with pytest.raises(ValueError):

        ModelRegistry.get_model(
            "invalid_model"
        )