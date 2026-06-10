import re
from sqlalchemy import text

from database.mysql import engine
from utils.sql_parser import clean_sql


# =========================
# Safety Check
# =========================
def validate_sql_safety(sql: str) -> bool:

    blocked = [
        "DROP",
        "TRUNCATE",
        "ALTER",
        "INSERT",
        "UPDATE",
        "DELETE",
        "CREATE",
        "REPLACE",
    ]

    sql_upper = sql.upper()

    return not any(word in sql_upper for word in blocked)


# =========================
# Forecast Validation
# =========================
def validate_forecast_sql(sql: str):

    errors = []

    sql_upper = sql.upper()

    if re.search(r"\b20\d{2}\b", sql):
        errors.append("Hardcoded year detected")

    if re.search(r"'\d{4}-\d{2}-\d{2}'", sql):
        errors.append("Hardcoded date detected")

    if "EXTRACT(MONTH" in sql_upper:
        errors.append("EXTRACT(MONTH) is not allowed")

    if re.search(r"\bMONTH\s*\(", sql_upper):
        errors.append("MONTH() is not allowed")

    if re.search(r"\bYEAR\s*\(", sql_upper):
        errors.append("YEAR() is not allowed")

    if "LIMIT" in sql_upper:
        errors.append("LIMIT is not allowed for forecasting datasets")

    forbidden_funcs = [
        "CURDATE(",
        "NOW(",
        "CURRENT_DATE",
        "CURRENT_TIMESTAMP",
        "DATE_SUB(",
        "DATE_ADD(",
    ]

    for func in forbidden_funcs:
        if func in sql_upper:
            errors.append(f"{func} is not allowed")

    if not re.search(r"\bAS\s+DS\b", sql_upper):
        errors.append("Missing alias: ds")

    if not re.search(r"\bAS\s+Y\b", sql_upper):
        errors.append("Missing alias: y")

    if "ORDER BY" in sql_upper and not re.search(
        r"ORDER\s+BY\s+DS",
        sql_upper,
    ):
        errors.append("Must ORDER BY ds")

    return errors


# =========================
# Validator
# =========================
def validator(state):

    sql = clean_sql(state.get("generated_sql", ""))

    forecast_flag = state.get("run_forecast", False)

    print("\n========== VALIDATOR ==========")
    print("SQL:", sql)
    print("FORECAST FLAG:", forecast_flag)

    if not sql:
        return {
            "validation": {
                "valid": False,
                "warnings": ["Empty SQL"],
            }
        }

    # Safety validation
    if not validate_sql_safety(sql):
        return {
            "validation": {
                "valid": False,
                "warnings": ["Unsafe SQL detected"],
            }
        }

    # Forecast validation
    if forecast_flag:

        errors = validate_forecast_sql(sql)

        if errors:
            return {
                "validation": {
                    "valid": False,
                    "warnings": errors,
                }
            }

    # SQL syntax validation
    try:

        with engine.connect() as conn:
            conn.execute(text(f"EXPLAIN {sql}"))

        return {
            "validation": {
                "valid": True,
                "warnings": [],
            }
        }

    except Exception as e:

        return {
            "validation": {
                "valid": False,
                "warnings": [str(e)],
            }
        }