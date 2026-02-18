SCHEMA = """
customers
- customer_id: unique customer identifier
- customer_city: city of the customer
- customer_state: state of the customer

orders
- order_id: unique order identifier
- customer_id: customer who placed the order
- order_status: status of the order
- order_purchase_timestamp: order creation timestamp

products
- product_id: unique product identifier
- product_category_name: category of the product

order_items
- order_item_id: unique item row (1 row = 1 product purchased)
- order_id: order identifier
- product_id: product identifier
- price: selling price of the product
- freight_value: shipping cost (not revenue)

Business rules:
- Each row in order_items = one product purchased
- Purchase count = COUNT(order_item_id)
- Order count = COUNT(DISTINCT order_id)
- Revenue/sales = SUM(price)

COLUMN OWNERSHIP RULES:
- orders.order_purchase_timestamp is the ONLY time column
- order_items has NO timestamp columns
- NEVER use oi.order_purchase_timestamp
- Apply join to access column from another table

Use table aliases strictly:
- orders AS o
- order_items AS oi
- products AS p

Valid columns:
- o.order_purchase_timestamp
- o.order_id
- oi.order_id
- oi.price

Time rules:
- Use orders.order_purchase_timestamp for all time-based analysis
- Monthly trend = DATE_TRUNC('month', order_purchase_timestamp)
- Yearly trend = DATE_TRUNC('year', order_purchase_timestamp)

- orders table does NOT contain product_id
- product_id exists ONLY in order_items
- Valid join paths:
  orders.order_id = order_items.order_id
  order_items.product_id = products.product_id
- prices come ONLY from order_items.price
"""
