import pandas as pd
from prophet import Prophet

def forecast_monthly_revenue(df: pd.DataFrame, periods: int = 3) -> pd.DataFrame:
    """
    df must have columns: ['month', 'revenue']
    """

    # Prepare data for Prophet
    ts = df.rename(columns={
        "month": "ds",
        "revenue": "y"
    })

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(ts)

    future = model.make_future_dataframe(
        periods=periods,
        freq="MS"   # Month Start
    )

    forecast = model.predict(future)

    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    result = result.rename(columns={
        "ds": "month",
        "yhat": "forecast",
        "yhat_lower": "lower_bound",
        "yhat_upper": "upper_bound"
    })

    return result
