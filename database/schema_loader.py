from sqlalchemy import inspect
from database.mysql import engine


def load_schema():

    inspector = inspect(engine)

    schema = []

    for table in inspector.get_table_names():

        table_block = []
        table_block.append(f"\nTABLE: {table}")

        # Columns
        columns = inspector.get_columns(table)

        for col in columns:
            col_type = str(col.get("type"))
            table_block.append(f"  - {col['name']} ({col_type})")

        # Primary Key
        pk = inspector.get_pk_constraint(table) or {}
        pk_cols = pk.get("constrained_columns") or []

        table_block.append(
            f"PRIMARY KEY: {pk_cols if pk_cols else 'NONE'}"
        )

        # Foreign Keys
        fks = inspector.get_foreign_keys(table) or []

        if not fks:
            table_block.append("FOREIGN KEYS: NONE")
        else:
            for fk in fks:
                table_block.append(
                    f"FOREIGN KEY: {fk.get('constrained_columns')} "
                    f"-> {fk.get('referred_table')}.{fk.get('referred_columns')}"
                )

        schema.append("\n".join(table_block))

    return "\n\n".join(schema)