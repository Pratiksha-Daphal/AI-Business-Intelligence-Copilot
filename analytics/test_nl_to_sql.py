# End-to-end NL → SQL → PostgreSQL test

from analytics.sql_generator import generate_sql
from analytics.db import run_sql

question = "Top 5 product categories by total revenue"

sql = generate_sql(question)
print("SQL:\n", sql)

df = run_sql(sql)
print(df.head())
