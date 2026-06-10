from config import llm
from pathlib import Path
from utils.sql_parser import clean_sql

PROMPT_PATH = Path("prompts/sql_prompt.txt")

def load_prompt():
    return PROMPT_PATH.read_text()

def sql_agent(state):
    schema = state.get("schema", "")
    question = state.get("user_query") or state.get("question")
    run_forecast = state.get("run_forecast", False)

    print("\n========== SQL AGENT ==========")
    print("FORECAST MODE:", run_forecast)
    print("QUESTION:", question)

    if not question:
        raise ValueError("Missing user query")

    base_prompt = load_prompt()

    prompt = base_prompt.format(
        schema=schema,
        question=question
    )

    draft_sql = llm.invoke(prompt).content
    draft_sql = clean_sql(draft_sql)

    print("\nSQL GENERATED:\n", draft_sql)

    return {
        **state,
        "generated_sql": draft_sql
    }