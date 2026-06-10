from database.schema_loader import load_schema

from agents.sql_agent import sql_agent

state = {

    "schema": load_schema(),

    "user_query":
    "Show total sales by region"
}

result = sql_agent(state)

print(result["generated_sql"])