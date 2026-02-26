import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI BI Copilot", layout="wide")
st.header("📊 AI Business Intelligence Copilot")

# ---------------- Session State ----------------
if "context" not in st.session_state:
    st.session_state.context = {
        "last_query": None,
        "last_sql": None,
        "last_summary": None
    }

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- Render Chat History ----------------
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):

        # USER MESSAGE
        if msg["role"] == "user":
            st.markdown(msg["content"])

        # ASSISTANT TEXT (greeting, clarification, business knowledge)
        elif msg.get("type") == "TEXT":
            st.markdown(msg["content"])

        # ASSISTANT ANALYTICS (FULL REPLAY)
        elif msg.get("type") == "ANALYTICS":
            if msg.get("sql"):
                with st.expander("Generated SQL"):
                    st.code(msg["sql"])

            df = pd.DataFrame(msg["data"])
            st.dataframe(df)

            # Auto chart for 2-column outputs
            if df.shape[1] == 2:
                st.bar_chart(df.set_index(df.columns[0]))

#input for voice query
# st.subheader("🎤 Ask by Voice (Live)")
SPEECH_URL = API_URL.replace("/chat", "") + "/speech"
audio = st.audio_input("Record your question")

if audio is not None:
    audio_bytes = audio.read()

    with st.spinner("Transcribing speech..."):
        response = requests.post(
            SPEECH_URL,
            files={"file": audio_bytes},
            timeout=120
        )

    if response.ok:
        recognized_text = response.json().get("text", "")
        if recognized_text:
            st.success(f"Recognized: {recognized_text}")
        else:
            st.warning("Speech not recognized. Please try again.")

        # Use transcribed text as query
        user_query = recognized_text


# st.subheader("🎤 Ask by voice")

audio_file = st.file_uploader(
    "Upload an audio query (wav/mp3)",
    type=["wav", "mp3"]
)

if audio_file is not None:
    audio_bytes = audio_file.read()

    with st.spinner("Transcribing audio..."):
        response = requests.post(
            f"{API_URL}/speech",
            files={"file": audio_bytes},
            timeout=120
        )

    if response.ok:
        query_text = response.json()["text"]
        if recognized_text:
            st.success(f"Recognized: {recognized_text}")
        else:
            st.warning("Speech not recognized. Please try again.")
        user_query = query_text


# ---------------- Chat Input ----------------
query = st.chat_input("Ask a business question")

if query:
    # Store user message
    st.session_state.history.append({
        "role": "user",
        "content": query
    })

    payload = {
        "query": query,
        "context": st.session_state.context
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json=payload, timeout=420)
            if not response.text.strip():
                st.error("Backend returned an empty response.")
                st.stop()

            try:
                result = response.json()
            except Exception:
                st.error("Backend returned invalid JSON.")
                st.text(response.text)
                st.stop()

        # -------- GREETING / CLARIFICATION / BUSINESS KNOWLEDGE --------
        response_type = result.get("type", "FALLBACK")

        if response_type in {"GREETING", "CLARIFICATION", "BUSINESS_KNOWLEDGE", "FALLBACK"}:

            st.markdown(result["message"])

            st.session_state.history.append({
                "role": "assistant",
                "type": "TEXT",
                "content": result["message"]
            })

        elif response_type == "FORECAST":
            hist_df = pd.DataFrame(result["historical"])
            forecast_df = pd.DataFrame(result["forecast"])

            st.subheader("Historical Revenue")
            st.line_chart(hist_df.set_index("month")["revenue"])

            st.subheader("Forecast (Next 3 Months)")
            st.dataframe(forecast_df)

            st.line_chart(
                forecast_df.set_index("month")[["forecast", "lower_bound", "upper_bound"]]
            )

            st.session_state.history.append({
                "role": "assistant",
                "type": "FORECAST",
                "historical": hist_df.to_dict(),
                "forecast": forecast_df.to_dict()
            })

            st.info(
                "This forecast is generated using Facebook Prophet based on historical monthly sales. "
                "It captures long-term trends and seasonality but does not account for external factors "
                "such as promotions or market changes."
                )
        # ---------------- ANALYTICS ----------------
        elif result["type"] == "ANALYTICS":
            df = pd.DataFrame(result["data"])

            if result.get("sql"):
                with st.expander("Generated SQL"):
                    st.code(result["sql"])

            st.dataframe(df)

            if df.shape[1] == 2:
                st.bar_chart(df.set_index(df.columns[0]))

            # UPDATE CONTEXT (unchanged logic)
            st.session_state.context.update({
                "last_query": query,
                "last_sql": result.get("sql"),
                "last_summary": df.describe().to_dict()
            })

            #  STORE FULL ANALYTICS MESSAGE
            st.session_state.history.append({
                "role": "assistant",
                "type": "ANALYTICS",
                "sql": result.get("sql"),
                "data": df.to_dict()
            })

        else:
            st.error(result.get("message", "Unknown backend error"))