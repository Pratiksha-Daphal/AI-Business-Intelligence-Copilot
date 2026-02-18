import uuid

# In-memory store for conversation history and context

class ConversationStore:
    def __init__(self):
        self.sessions = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "history": [],
            "last_metrics": [],
            "last_filters": {}
        }
        return session_id

    def add_message(self, session_id, role, content):
        self.sessions[session_id]["history"].append({
            "role": role,
            "content": content
        })

    def get_context(self, session_id):
        return self.sessions.get(session_id, {})
