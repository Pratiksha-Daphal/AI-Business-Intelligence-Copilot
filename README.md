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
<img width="1920" height="1080" alt="Time series based Analytics" src="https://github.com/user-attachments/assets/2ff66942-b4d8-491e-a532-c84d99e8df45" />
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
<img width="1767" height="603" alt="business knowledge" src="https://github.com/user-attachments/assets/fb4d34c5-f184-42b6-a888-7108fd9b1270" />
Examples:

Monthly revenue trends

Yearly revenue summary

Top-performing categories

Charts and tables are automatically generated.

🔁 Contextual Follow-Up Questions
<!-- Add follow-up interaction screenshot -->
<img width="1920" height="903" alt="Context based Analytics" src="https://github.com/user-attachments/assets/954e14e9-0405-4cc8-8186-02cfc31027d1" />
After an analysis, users can ask:

“Why did it drop?”

“Which month performed worst?”

The system uses active session context to answer intelligently.

🔮 Forecasting (Time-Series)
<!-- Add forecast chart screenshot -->
<img width="1920" height="1080" alt="Forecasting" src="https://github.com/user-attachments/assets/56eca29c-53c6-47d7-b47d-8f737d8b250c" />

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
