# forecasting/xgboost_forecaster.py

import pandas as pd
import xgboost as xgb


class XGBoostForecaster:

    def forecast(
        self,
        df: pd.DataFrame,
        date_col: str,
        value_col: str,
        periods: int = 30
    ):

        data = df.copy()

        data["day"] = pd.to_datetime(
            data[date_col]
        ).dt.dayofyear

        X = data[["day"]]
        y = data[value_col]

        model = xgb.XGBRegressor(
            n_estimators=200,
            learning_rate=0.05
        )

        model.fit(X, y)

        last_day = X["day"].max()

        future_days = pd.DataFrame({
            "day": range(
                last_day + 1,
                last_day + periods + 1
            )
        })

        predictions = model.predict(
            future_days
        )

        return pd.DataFrame({
            "forecast": predictions
        })