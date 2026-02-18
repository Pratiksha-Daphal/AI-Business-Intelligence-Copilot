from llm.ollama_client import call_llama

BUSINESS_QA_PROMPT = """
You are a senior business analyst.

Answer the following question clearly and concisely
in non-technical business language.

Do NOT reference any database or dataset.

Question:
{question}
"""

def answer_business_question(question: str) -> str:
    prompt = BUSINESS_QA_PROMPT.format(question=question)
    return call_llama(prompt).strip()
