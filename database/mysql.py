import pandas as pd
from sqlalchemy import create_engine, text

from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
from utils.sql_parser import clean_sql


# -----------------------------
# ENGINE (NO IMPORT FROM SAME MODULE)
# -----------------------------
connection_string = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(connection_string)


# -----------------------------
# EXECUTE SQL SAFELY
# -----------------------------
def execute_sql(query: str):

    query = clean_sql(query)
    query = query.replace("```sql", "").replace("```", "").strip()

    if not query:
        raise ValueError("Empty SQL after cleaning")

    df = pd.read_sql(text(query), engine)

    # 🔥 FIX: prevent downstream forecast crash
    if df is None or df.empty:
        return pd.DataFrame(columns=["ds", "y"])

    return df