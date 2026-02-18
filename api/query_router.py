def is_greeting(query: str) -> bool:
    return query.lower() in {"hi", "hello", "hey", "good morning", "good evening"}

def is_followup_question(query: str) -> bool:
    return any(w in query.lower() for w in ["why", "explain", "reason", "what happened"])

def is_analytics_query(query: str) -> bool:
    keywords = ["revenue", "sales", "orders", "trend", "top", "count", "monthly", "yearly", "forecast"]
    return any(k in query.lower() for k in keywords)

def is_business_knowledge(query: str) -> bool:
    keywords = ["what is","Which","business", "difference", "define", "kpi", "profit", "margin", "churn"]
    return any(k in query.lower() for k in keywords)

def is_incomplete_followup(query: str) -> bool:
    return query.lower().strip() in {"monthly", "yearly", "daily"}