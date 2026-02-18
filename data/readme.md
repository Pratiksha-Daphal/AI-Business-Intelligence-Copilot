# Data Directory – Olist Brazilian E-Commerce Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, a real-world e-commerce dataset containing ~100k orders from a Brazilian marketplace.

The dataset is used as the backend data source for the **AI Business Intelligence Chatbot**, enabling realistic analytics and natural-language-to-SQL queries.

---

## Dataset Source

- Platform: Kaggle
- Dataset name: Brazilian E-Commerce Public Dataset (Olist)
- Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---

## Tables Used (Phase 1 – Core BI)

Only a subset of tables is used initially to keep the BI model clean and incremental.

### customers
Customer location and identity information.

Key columns:
- customer_id
- customer_city
- customer_state

---

### orders
Order-level transactional data.

Key columns:
- order_id
- customer_id
- order_status
- order_purchase_timestamp

---

### order_items
Line-item level sales data (fact table).

Key columns:
- order_id
- product_id
- price
- freight_value

---

### products
Product-level attributes.

Key columns:
- product_id
- product_category_name

---

## Why Incremental Table Selection

The database schema is built incrementally to mirror real BI system design:

- Phase 1: Revenue, product, and customer analytics
- Phase 2 (future): Payments and reviews
- Phase 3 (optional): Sellers and geolocation

This approach improves maintainability, query performance, and explainability.

---

## Data Storage

- Raw CSV files are **not committed** to this repository.
- Data is loaded into a local **PostgreSQL** database (`olist_bi`).
- SQL execution is restricted to **read-only SELECT queries**.

---

## Usage in Project

The dataset powers:
- Natural Language → SQL generation using LLaMA
- PostgreSQL-based analytics
- Business intelligence queries
- Streamlit visualizations

---

## Disclaimer

This dataset is publicly available and used strictly for educational and portfolio purposes.
