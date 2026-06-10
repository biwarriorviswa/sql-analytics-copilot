from database.mysql import execute_sql

df = execute_sql(
    "SELECT * FROM sales"
)

print(df)