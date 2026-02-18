# Executes read-only SQL queries on PostgreSQL

import psycopg2
import pandas as pd
import re

def run_sql(sql: str) -> pd.DataFrame:
    # Remove markdown fences and extra text
    sql = re.sub(r"```.*?\n", "", sql, flags=re.DOTALL).replace("```", "").strip()
    sql = sql.rstrip(";")

    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries allowed")
    if "from" not in sql.lower():
        raise ValueError("Invalid SQL: missing FROM clause")

    conn = psycopg2.connect(
        host="localhost",
        database="olist_bi",
        user="postgres",
        password="postgres"
    )

    df = pd.read_sql(sql, conn)
    conn.close()
    return df
