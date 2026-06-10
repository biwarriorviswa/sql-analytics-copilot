# forecasting/model_registry.py

from forecasting.prophet_forecaster import ProphetForecaster
from forecasting.xgboost_forecaster import XGBoostForecaster


class ModelRegistry:

    MODELS = {
        "prophet": ProphetForecaster,
        "xgboost": XGBoostForecaster
    }

    @classmethod
    def get_model(cls, model_name: str):

        model = cls.MODELS.get(model_name)

        if not model:
            raise ValueError(f"Unknown model: {model_name}")

        return model()