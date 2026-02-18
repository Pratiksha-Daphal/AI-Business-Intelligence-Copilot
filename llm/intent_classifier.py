from llm.ollama_client import call_llama
from llm.prompts import INTENT_PROMPT

SQL_KEYWORDS = [
    "top", "most", "least", "count", "sum", "average",
    "revenue", "orders", "purchased", "sales",
    "category", "product", "state", "city", "trend",
    "show", "list", "which"
]

def looks_like_sql_query(query: str) -> bool:
    q = query.lower()
    return any(word in q for word in SQL_KEYWORDS)

def classify_intent(query: str) -> str:
    # Rule-based override for BI queries
    if looks_like_sql_query(query):
        return "SQL_QUERY"

    # Fallback to LLM classification
    prompt = INTENT_PROMPT.format(question=query)
    intent = call_llama(prompt).strip().upper()

    if intent not in {"SQL_QUERY", "DOCUMENT_QA", "FORECAST", "GENERAL"}:
        return "GENERAL"

    return intent
