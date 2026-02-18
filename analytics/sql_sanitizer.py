import re

def sanitize_sql(sql: str) -> str:
    # Remove markdown
    sql = re.sub(r"```.*?\n", "", sql, flags=re.DOTALL)
    sql = sql.replace("```", "")

    # Remove ALL semicolons
    sql = sql.replace(";", "")

    # Collapse whitespace
    sql = re.sub(r"\s+", " ", sql).strip()

    return sql
