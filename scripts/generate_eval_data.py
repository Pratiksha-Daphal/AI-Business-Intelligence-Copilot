import json
import random

OUTPUT_FILE = "data/nl_sql_eval.jsonl"

SCHEMA = """
orders(order_id, order_date)
order_items(order_id, price)
"""

EVAL_QUESTIONS = {
    "monthly_trend": [
        "Show month-wise revenue growth",
        "Revenue trend across months",
        "How has revenue evolved monthly?"
    ],
    "yearly_trend": [
        "Annual sales trend",
        "How does revenue vary year by year?"
    ],
    "filtered_revenue": [
        "Revenue after {year}",
        "Total revenue since {year}"
    ],
    "top_months": [
        "Most profitable {n} months",
        "Top performing {n} months by revenue"
    ]
}

def sql_monthly():
    return """
SELECT DATE_TRUNC('month', o.order_date) AS month,
       SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;
"""

def sql_yearly():
    return """
SELECT DATE_TRUNC('year', o.order_date) AS year,
       SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY year
ORDER BY year;
"""

def sql_filtered(year):
    return f"""
SELECT SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '{year}-01-01';
"""

def sql_top(n):
    return f"""
SELECT DATE_TRUNC('month', o.order_date) AS month,
       SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY revenue DESC
LIMIT {n};
"""

records = []

for _ in range(30):
    intent = random.choice(list(EVAL_QUESTIONS.keys()))
    template = random.choice(EVAL_QUESTIONS[intent])

    if intent == "filtered_revenue":
        year = random.choice([2017, 2018, 2019])
        question = template.format(year=year)
        sql = sql_filtered(year)

    elif intent == "top_months":
        n = random.choice([3, 5])
        question = template.format(n=n)
        sql = sql_top(n)

    elif intent == "monthly_trend":
        question = template
        sql = sql_monthly()

    else:
        question = template
        sql = sql_yearly()

    records.append({
        "question": question,
        "schema": SCHEMA,
        "gold_sql": sql.strip()
    })

with open(OUTPUT_FILE, "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

print("✅ Generated evaluation dataset (30 samples)")
