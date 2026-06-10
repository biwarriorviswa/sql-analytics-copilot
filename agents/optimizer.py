from config import llm
from utils.sql_parser import clean_sql


def optimizer(state):

    generated_sql = state.get("generated_sql")
    user_query = state.get("user_query")

    print("\n================ OPTIMIZER ================")
    print("INPUT SQL:", generated_sql)

    if not generated_sql:
        return {
            **state,
            "optimized_sql": None,
            "optimizer_metadata": {"error": "Missing SQL"}
        }

    prompt = f"""
You are ONLY a SQL syntax fixer.

STRICT RULES:
1. DO NOT add new columns
2. DO NOT add calculations not in input
3. DO NOT modify business logic
4. DO NOT create forecasting logic
5. ONLY fix syntax errors
6. Return ONLY SQL

User Question:
{user_query}

SQL:
{generated_sql}
"""

    response = llm.invoke(prompt)
    raw = response.content if hasattr(response, "content") else str(response)

    optimized_sql = clean_sql(raw) or generated_sql

    print("\nOUTPUT SQL:", optimized_sql)

    return {
        **state,
        "optimized_sql": optimized_sql,
        "optimizer_metadata": {
            "optimized": False
        }
    }