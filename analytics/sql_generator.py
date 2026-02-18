from llm.ollama_client import call_llama
from analytics.schema import SCHEMA
from llm.prompts import SQL_PROMPT

def generate_sql(question: str, context: dict | None = None) -> str:
    context_text = ""

    if context and context.get("last_query"):
        context_text = f"""
Previous question:
{context['last_query']}

Previous SQL:
{context['last_sql']}
"""

    prompt = SQL_PROMPT.format(
        schema=SCHEMA,
        question=context_text + "\n" + question
    )

    return call_llama(prompt).strip()
