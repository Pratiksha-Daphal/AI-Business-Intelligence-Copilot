def derive_insights(df):
    insights = []

    if "revenue" in df.columns:
        if df["revenue"].iloc[-1] < df["revenue"].iloc[0]:
            insights.append(
                "Revenue shows a declining trend. This may indicate pricing pressure, demand drop, or increased competition."
            )

    if len(df) > 1:
        insights.append(
            "Consider drilling down by category or region to identify underlying drivers."
        )

    return insights
