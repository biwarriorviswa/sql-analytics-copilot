from database.schema_loader import load_schema
from database.mysql import execute_sql

from agents.sql_agent import sql_agent
from agents.validator import validator
from agents.optimizer import optimizer

from agents.analytics_agent import analytics_agent
from agents.insight_agent import insight_agent

from agents.forecast_detector import forecast_detector
from agents.forecast_agent import forecast_agent


print("\n" + "=" * 100)
print("PHASE 1 → PHASE 3 PIPELINE TEST")
print("=" * 100)

# ------------------------------------------------------------------
# SCHEMA
# ------------------------------------------------------------------

schema = load_schema()

print("\nSCHEMA")
print("-" * 100)
print(schema)

# ------------------------------------------------------------------
# STATE INIT
# ------------------------------------------------------------------

state = {
    "schema": schema,
    "user_query": "Show last 6 months sales trend by month and forecast next 6 months"
}

print("\nUSER QUERY")
print("-" * 100)
print(state["user_query"])

# ------------------------------------------------------------------
# SQL AGENT
# ------------------------------------------------------------------

state.update(sql_agent(state))

print("\nGENERATED SQL")
print("-" * 100)
print(state["generated_sql"])

# ------------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------------

state = validator(state)

print("\nVALIDATION")
print("-" * 100)
print(state.get("validation"))

# ------------------------------------------------------------------
# OPTIMIZER (if needed)
# ------------------------------------------------------------------

if not state.get("validation", {}).get("valid", True):

    state.update(optimizer(state))

    state["generated_sql"] = state["optimized_sql"]

    state = validator(state)

    if not state["validation"]["valid"]:
        raise Exception(state["validation"]["warnings"])

else:
    state["optimized_sql"] = state["generated_sql"]

# ------------------------------------------------------------------
# EXECUTE SQL
# ------------------------------------------------------------------

df = execute_sql(state["optimized_sql"])

state["data"] = df

print("\nDATA PREVIEW")
print("-" * 100)
print(df.head())

# ------------------------------------------------------------------
# ANALYTICS
# ------------------------------------------------------------------

state.update(analytics_agent(state))

print("\nANALYTICS")
print("-" * 100)
print(state["analytics"])

# ------------------------------------------------------------------
# INSIGHTS
# ------------------------------------------------------------------

state.update(insight_agent(state))

print("\nINSIGHTS")
print("-" * 100)
print(state["insights"])

# ------------------------------------------------------------------
# FORECAST DETECTOR
# ------------------------------------------------------------------

state.update(forecast_detector(state))

forecast_required = state.get("forecast_required", False)

print("\nFORECAST REQUIRED")
print("-" * 100)
print(forecast_required)

# ------------------------------------------------------------------
# FORECAST AGENT
# ------------------------------------------------------------------

if forecast_required:

    print("\nRUNNING FORECAST")
    print("-" * 100)

    state["model_name"] = "prophet"
    state["periods"] = 6

    result = forecast_agent(state)
    state.update(result)

    print("\nFORECAST OUTPUT")
    print("-" * 100)

    print(state.get("forecast"))

# ------------------------------------------------------------------
# DONE
# ------------------------------------------------------------------

print("\n" + "=" * 100)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 100)