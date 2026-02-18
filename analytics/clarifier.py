def needs_clarification(query: str) -> str | None:
    q = query.lower()

    # Ambiguous time
    if "revenue" in q and not any(t in q for t in ["month", "year", "daily"]):
        return "For which time period should I analyze revenue (monthly or yearly)?"

    # Ambiguous product reference
    if "product" in q and "category" not in q:
        return (
            "This dataset contains product categories, not individual product names. "
            "Should I analyze product categories?"
        )

    # Forecast horizon missing
    if "forecast" in q and not any(t in q for t in ["next", "future"]):
        return "How far ahead should I forecast (e.g., next 3 months)?"

    return None
