# analytics/sql_engine.py

from analytics.db import run_sql
from analytics.sql_sanitizer import sanitize_sql
from analytics.sql_validator import validate_and_fix_sql

def execute_sql(sql: str):
    # 1️⃣ Remove markdown, semicolons, bad formatting
    sql = sanitize_sql(sql)

    # 2️⃣ Validate + auto-fix SQL
    sql = validate_and_fix_sql(sql)

    # 3️⃣ Execute safely
    return run_sql(sql)
