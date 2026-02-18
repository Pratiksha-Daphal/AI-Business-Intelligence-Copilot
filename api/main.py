from fastapi import FastAPI
from typing import Dict, Any
import traceback
from analytics.forecast_engine import forecast_monthly_revenue
from fastapi import UploadFile, File
from multimodal.speech_to_text import speech_to_text

from api.query_router import (
    is_greeting,
    is_analytics_query,
    is_business_knowledge,
    is_followup_question
)
from analytics.clarifier import needs_clarification
from analytics.sql_generator import generate_sql
from analytics.sql_engine import execute_sql
from llm.business_qa import answer_business_question
from llm.insight_qa import answer_analytics_followup

app = FastAPI()

@app.post("/speech")
async def speech_query(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    text = speech_to_text(audio_bytes)

    if not text:
        return {
            "type": "ERROR",
            "message": "Could not recognize speech. Please try speaking clearly."
        }

    return {"text": text}


@app.post("/chat")
def chat(payload: Dict[str, Any]):
    try:
        query = payload.get("query", "").strip()
        context = payload.get("context", {})

        # 1️⃣ Greeting
        if is_greeting(query):
            return {
                "type": "GREETING",
                "message": "Hi! I can help analyze business data, forecast trends, or explain business concepts."
            }

        # 2️⃣ Business knowledge
        if is_business_knowledge(query):
            return {
                "type": "BUSINESS_KNOWLEDGE",
                "message": answer_business_question(query)
            }

        # 3️⃣ Follow-up explanation
        if is_followup_question(query):
            if not context.get("last_summary"):
                return {
                    "type": "CLARIFICATION",
                    "message": "Please run an analysis first so I can explain the results."
                }

            explanation = answer_analytics_followup(
                query=query,
                summary=context["last_summary"]
            )

            return {
                "type": "BUSINESS_KNOWLEDGE",
                "message": explanation
            }

        # 4️⃣ Clarification (analytics only)
        clarification = needs_clarification(query)
        if clarification:
            return {
                "type": "CLARIFICATION",
                "message": clarification
            }
        
        if "forecast" in query.lower():
            sql = """
            SELECT
            DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
            SUM(oi.price) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY month
            ORDER BY month;
            """

            df = execute_sql(sql)

            forecast_df = forecast_monthly_revenue(df, periods=3)

            return {
                "type": "FORECAST",
                "historical": df.to_dict(),
                "forecast": forecast_df.tail(3).to_dict()
            }

        # 5️⃣ Analytics
        if is_analytics_query(query):
            sql = generate_sql(query, context)
            df = execute_sql(sql)

            return {
                "type": "ANALYTICS",
                "sql": sql,
                "data": df.head(100).to_dict()
            }

        # 6️⃣ Fallback
        return {
            "type": "FALLBACK",
            "message": "I can help with business analytics, forecasting, or business concepts. Please rephrase."
        }

    except Exception as e:
        # 🔥 CRITICAL: never crash silently
        traceback.print_exc()

        return {
            "type": "ERROR",
            "message": str(e)
        }
