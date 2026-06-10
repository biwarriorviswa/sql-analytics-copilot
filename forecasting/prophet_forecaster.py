# forecasting/prophet_forecaster.py

import pandas as pd
from prophet import Prophet

class ProphetForecaster:


    def _detect_frequency(self, dates: pd.Series) -> str:
        """
        Detect time series frequency.
        """

        dates = pd.to_datetime(dates).sort_values()

        freq = pd.infer_freq(dates)

        if freq:
            if freq.startswith("M"):
                return "MS"
            return freq

        avg_gap = dates.diff().dt.days.dropna().mean()

        if pd.isna(avg_gap):
            return "D"

        if avg_gap >= 27:
            return "MS"
        elif avg_gap >= 6:
            return "W"
        else:
            return "D"

    def forecast(
        self,
        df: pd.DataFrame,
        date_col: str,
        value_col: str,
        periods: int = 30
    ) -> pd.DataFrame:

        if df.empty:
            return pd.DataFrame()

        prophet_df = df[[date_col, value_col]].copy()

        prophet_df.columns = ["ds", "y"]

        prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

        prophet_df = (
            prophet_df
            .dropna(subset=["ds", "y"])
            .sort_values("ds")
        )

        if len(prophet_df) < 2:
            return pd.DataFrame()

        freq = self._detect_frequency(prophet_df["ds"])

        n_obs = len(prophet_df)

        # Prevent negative forecasts
        prophet_df["floor"] = 0
        prophet_df["cap"] = prophet_df["y"].max() * 2

        # Configure Prophet based on available history
        if n_obs < 24:
            model = Prophet(
                growth="logistic",
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
        else:
            model = Prophet(
                growth="logistic",
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )

        model.fit(prophet_df)

        future = model.make_future_dataframe(
            periods=periods,
            freq=freq
        )

        future["floor"] = 0
        future["cap"] = prophet_df["cap"].iloc[0]

        forecast = model.predict(future)

        forecast = forecast[
            forecast["ds"] > prophet_df["ds"].max()
        ].copy()

        # Safety: no negative sales
        forecast["yhat"] = forecast["yhat"].clip(lower=0)
        forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)
        forecast["yhat_upper"] = forecast["yhat_upper"].clip(lower=0)

        return forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].reset_index(drop=True)

