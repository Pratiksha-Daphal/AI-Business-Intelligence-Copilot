# AI-Business-Intelligence-Copilot
AI-powered Business Intelligence Copilot with conversational analytics, forecasting, and multimodal voice queries using FastAPI, Streamlit, PostgreSQL, and LLMs.


📊 AI Business Intelligence Copilot

An AI-powered Business Intelligence Copilot that allows users to interact with business data using natural language and voice, generate analytics, visualize insights, ask contextual follow-up questions, and forecast future sales using time-series models.

This project is built with a production-style GenAI architecture, focusing on reliability, explainability, and real enterprise BI use cases.

🚀 Key Highlights

🔹 Natural Language → SQL analytics

🔹 Conversational BI with follow-up questions

🔹 Business knowledge Q&A

🔹 Revenue forecasting using time-series models

🔹 Multimodal input: Text + Live Voice Queries

🔹 Robust backend & frontend error handling

🖥️ Application Overview
🏠 Main Chat Interface
<!-- Add screenshot of main UI -->

Users can ask questions in plain English (or via voice) and receive:

tables

charts

business explanations

🎤 Voice-Enabled Queries (Multimodal)
<!-- Add screenshot of mic recording -->

Users can speak queries such as:

“Forecast monthly revenue for the next three months”

Speech is transcribed and processed through the same BI pipeline.

📈 Business Intelligence & Analytics
<!-- Add analytics chart screenshot -->

Examples:

Monthly revenue trends

Yearly revenue summary

Top-performing categories

Charts and tables are automatically generated.

🔁 Contextual Follow-Up Questions
<!-- Add follow-up interaction screenshot -->

After an analysis, users can ask:

“Why did it drop?”

“Which month performed worst?”

The system uses active session context to answer intelligently.

🔮 Forecasting (Time-Series)
<!-- Add forecast chart screenshot -->

Forecasts monthly revenue for the next 3 months

Uses historical data and time-series modeling

Displays predicted values with confidence bounds

Clear business explanation of assumptions

🧠 How It Works (Architecture)
User (Text / Voice)
        ↓
Input Preprocessing (Speech → Text)
        ↓
Intent Routing & Clarification
        ↓
 ┌───────────────┬───────────────────┐
 │               │                   │
Analytics     Forecasting      Business Knowledge
 │               │                   │
NL → SQL     Time-Series Model        LLM
 │               │
PostgreSQL   Predictions
 │               │
Tables • Charts • Explanations

🛠️ Tech Stack

Python

FastAPI – backend API

Streamlit – frontend UI

PostgreSQL – analytics database

LLMs (via Ollama / pluggable) – NL → SQL & explanations

Whisper (Speech-to-Text) – voice input

Pandas / NumPy – data processing

Matplotlib / Streamlit charts – visualization
