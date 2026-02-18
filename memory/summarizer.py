def summarize_context(context: dict) -> str:
    history = context.get("history", [])[-5:]

    summary = "Conversation context:\n"
    for h in history:
        summary += f"{h['role']}: {h['content']}\n"

    return summary
