def plan_execution(intent: str, query: str) -> dict:
    """
    Decides what pipeline to use
    """
    if intent == "SQL_QUERY":
        return {
            "pipeline": "sql",
            "explain": False
        }

    if intent == "DOCUMENT_QA":
        return {
            "pipeline": "explain_only"
        }

    if intent == "FORECAST":
        return {
            "pipeline": "forecast"
        }

    return {
        "pipeline": "general"
    }
