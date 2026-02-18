from llm.ollama_client import call_llama
from llm.prompts import EXPLAIN_PROMPT

def explain_result(df, question: str) -> str:
    summary = df.describe(include="all").to_string()

    prompt = EXPLAIN_PROMPT.format(
        data=summary,
        question=question
    )

    return call_llama(prompt).strip()
