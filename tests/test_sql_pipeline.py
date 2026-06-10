from database.schema_loader import load_schema

from agents.sql_agent import sql_agent

from agents.validator import validator

from agents.optimizer import optimizer

from database.mysql import execute_sql


state = {

    "schema": load_schema(),

    "user_query":
    "Show total sales by region"
}


# Generate SQL
state.update(
    sql_agent(state)
)

# Validate

print(state["generated_sql"])
validator(state)

# Optimize
state.update(
    optimizer(state)
)

print("\nOptimized SQL:\n")

print(
    state["optimized_sql"]
)

# Execute
df = execute_sql(
    state["optimized_sql"]
)

print("\nResults:\n")

print(df)