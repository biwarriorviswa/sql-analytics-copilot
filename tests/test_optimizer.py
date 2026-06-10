from agents.optimizer import optimizer

state = {

    "generated_sql":
    """
    SELECT
        c.region,
        SUM(s.sales_amount) AS total_sales
    FROM customers c
    JOIN sales s
        ON c.customer_id = s.customer_id
    GROUP BY c.region
    """
}

result = optimizer(state)

print(result["optimized_sql"])