import re


def clean_sql(sql_text: str) -> str:
    """
    Robust SQL cleaner for LLM outputs.
    Removes markdown, explanations, and ensures clean executable SQL.
    """

    if not sql_text:
        return ""

    sql_text = str(sql_text).strip()

    # --------------------------------------------------
    # 1. Remove markdown code blocks
    # --------------------------------------------------
    sql_text = re.sub(r"```sql", "", sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r"```", "", sql_text)

    # --------------------------------------------------
    # 2. Extract first valid SQL statement
    # --------------------------------------------------
    match = re.search(
        r"\b(SELECT|WITH|INSERT|UPDATE|DELETE)\b.*",
        sql_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return ""

    sql_text = match.group(0)

    # --------------------------------------------------
    # 3. Remove trailing non-SQL garbage
    #    (cuts off after last semicolon or end)
    # --------------------------------------------------
    sql_text = sql_text.strip()

    # keep only first statement if multiple exist
    parts = sql_text.split(";")
    sql_text = parts[0]

    # --------------------------------------------------
    # 4. Fix common spacing issues
    # --------------------------------------------------
    sql_text = re.sub(r"\s+", " ", sql_text)          # normalize spaces
    sql_text = re.sub(r"\s+FROM", " FROM", sql_text)
    sql_text = re.sub(r"\s+WHERE", " WHERE", sql_text)
    sql_text = re.sub(r"\s+GROUP", " GROUP", sql_text)
    sql_text = re.sub(r"\s+ORDER", " ORDER", sql_text)

    # --------------------------------------------------
    # 5. Remove trailing commas before FROM/WHERE
    # --------------------------------------------------
    sql_text = re.sub(r",\s*FROM", " FROM", sql_text)

    # --------------------------------------------------
    # 6. Final cleanup
    # --------------------------------------------------
    sql_text = sql_text.strip()

    return sql_text