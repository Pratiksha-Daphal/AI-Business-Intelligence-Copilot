import json
import random

OUTPUT_FILE = "data/nl_sql_train.jsonl"

SCHEMA = """
orders(order_id, order_date)
order_items(order_id, price)
"""

# Question paraphrases grouped by intent
QUESTION_TEMPLATES = {
    "monthly_trend": [
        "Show monthly revenue trend",
        "Monthly revenue analysis",
        "How does revenue change month over month?",
        "Revenue trend by month",
        "Monthly sales trend"
    ],
    "yearly_trend": [
        "Show yearly revenue trend",
        "Annual revenue analysis",
        "Revenue by year",
        "Year-wise revenue trend"
    ],
    "total_revenue": [
        "What is the total revenue?",
        "Total sales value",
        "Overall revenue generated"
    ],
    "top_months": [
        "Top {n} months by revenue",
        "Highest {n} revenue months",
        "Which {n} months generated the most revenue?"
    ],
    "avg_monthly": [
        "Average monthly revenue",
        "Mean revenue per month",
        "What is the average monthly sales value?"
    ]
}

def sql_monthly_trend(alias_o, alias_oi, order):
    return f"""
SELECT DATE_TRUNC('month', {alias_o}.order_date) AS month,
       SUM({alias_oi}.price) AS revenue
FROM orders {alias_o}
JOIN order_items {alias_oi} ON {alias_o}.order_id = {alias_oi}.order_id
GROUP BY month
ORDER BY month {order};
"""

def sql_yearly_trend(alias_o, alias_oi):
    return f"""
SELECT DATE_TRUNC('year', {alias_o}.order_date) AS year,
       SUM({alias_oi}.price) AS revenue
FROM orders {alias_o}
JOIN order_items {alias_oi} ON {alias_o}.order_id = {alias_oi}.order_id
GROUP BY year
ORDER BY year;
"""

def sql_total_revenue(alias_o, alias_oi):
    return f"""
SELECT SUM({alias_oi}.price) AS revenue
FROM orders {alias_o}
JOIN order_items {alias_oi} ON {alias_o}.order_id = {alias_oi}.order_id;
"""

def sql_top_months(alias_o, alias_oi, n):
    return f"""
SELECT DATE_TRUNC('month', {alias_o}.order_date) AS month,
       SUM({alias_oi}.price) AS revenue
FROM orders {alias_o}
JOIN order_items {alias_oi} ON {alias_o}.order_id = {alias_oi}.order_id
GROUP BY month
ORDER BY revenue DESC
LIMIT {n};
"""

def sql_avg_monthly(alias_o, alias_oi):
    return f"""
SELECT AVG(monthly_revenue)
FROM (
    SELECT DATE_TRUNC('month', {alias_o}.order_date) AS month,
           SUM({alias_oi}.price) AS monthly_revenue
    FROM orders {alias_o}
    JOIN order_items {alias_oi} ON {alias_o}.order_id = {alias_oi}.order_id
    GROUP BY month
) sub;
"""

SQL_GENERATORS = {
    "monthly_trend": sql_monthly_trend,
    "yearly_trend": sql_yearly_trend,
    "total_revenue": sql_total_revenue,
    "top_months": sql_top_months,
    "avg_monthly": sql_avg_monthly
}

def generate_examples(target=100):
    examples = set()
    records = []

    while len(records) < target:
        intent = random.choice(list(QUESTION_TEMPLATES.keys()))
        question_template = random.choice(QUESTION_TEMPLATES[intent])

        alias_o = random.choice(["o", "ord"])
        alias_oi = random.choice(["oi", "items"])

        if intent == "top_months":
            n = random.choice([3, 5, 10])
            question = question_template.format(n=n)
            sql = SQL_GENERATORS[intent](alias_o, alias_oi, n)
        elif intent == "monthly_trend":
            order = random.choice(["ASC", "DESC"])
            question = question_template
            sql = SQL_GENERATORS[intent](alias_o, alias_oi, order)
        else:
            question = question_template
            sql = SQL_GENERATORS[intent](alias_o, alias_oi)

        key = (question.strip(), sql.strip())
        if key in examples:
            continue

        examples.add(key)
        records.append({
            "instruction": "Generate a SQL query for the business question using the given schema.",
            "input": f"Question: {question}\nSchema:\n{SCHEMA}",
            "output": sql.strip()
        })

    return records

data = generate_examples(100)

with open(OUTPUT_FILE, "w") as f:
    for row in data:
        f.write(json.dumps(row) + "\n")

print(f"✅ Generated {len(data)} diverse NL-to-SQL training examples.")
