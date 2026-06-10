print("Starting test...")

from agents.validator import validator

state = {
    "generated_sql": """
    SELECT *
    FROM sales
    """
}

try:
    result = validator(state)
    print("Validator returned:", result)
    print("PASS: Valid SQL")

except Exception as e:
    print("FAIL:", e)

print("Test finished")