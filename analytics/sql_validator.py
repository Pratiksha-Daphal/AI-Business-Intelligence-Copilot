# analytics/sql_validator.py

import re

# Only block obviously hallucinated columns
FORBIDDEN_PATTERNS = [
    "product_name",      # known hallucination
    "order_date",        # not in schema
    "total_revenue",     # computed alias sometimes misused
]

def validate_and_fix_sql(sql: str) -> str:
    sql_lower = sql.lower()

    # Enforce SELECT-only
    if not sql_lower.strip().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    # Catch known hallucinations (lightweight)
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in sql_lower:
            raise ValueError(f"Invalid SQL generated: hallucinated column '{pattern}'")

    return sql
