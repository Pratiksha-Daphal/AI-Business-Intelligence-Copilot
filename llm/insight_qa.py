from llm.ollama_client import call_llama

INSIGHT_PROMPT = """
You are a senior business analyst.

Based on the analytics summary below, answer the user's question
in clear business language. Do NOT invent data.

Analytics summary:
{summary}

User question:
{question}
"""

def answer_analytics_followup(question: str, summary: dict) -> str:
    prompt = INSIGHT_PROMPT.format(
        summary=summary,
        question=question
    )
    return call_llama(prompt).strip()
