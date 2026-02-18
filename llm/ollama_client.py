# Ollama client wrapper (safe for generate + chat APIs)

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def call_llama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

    data = response.json()

    # Ollama /api/generate returns text under "response"
    if "response" in data:
        return data["response"]

    # Fallback (future-proofing)
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]

    raise ValueError(f"Unexpected Ollama response format: {data}")
