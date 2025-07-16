from typing import List
from sql_composer.db_models import Table, Column, PgDataTypes
import textwrap

class SqlComposerPg:
    def __init__(self, table: Table):
        self.table = table

    def select(
        self, columns: List[Column] | None = None, alias: str | None = None
    ) -> str:
        if columns is None:
            col_names = [c.name for c in self.table.columns]
        else:
            col_names_set = set([c.name for c in columns])
            col_names = [c.name for c in self.table.columns if c.name in col_names_set]

        if alias is None:
            table_name = self.table.name
            col_names_fmted = ", ".join(col_names)
        else:
            table_name = f"{self.table.name} AS {alias}"
            col_names_fmted = ", ".join([f"{alias}.{c_name}" for c_name in col_names])

        stmt = f"""
        SELECT 
            {col_names_fmted}
        FROM {table_name}
        ;
        """

        return textwrap.dedent(stmt)

    def insert(self, key_values: dict[str, any]):
        column_map = {c.name: c for c in self.table.columns}

        col_names = [f"'{k}'" for k in key_values.keys()]
        col_values = [
            SqlComposerPg.to_expr(column_map[col_name], value)
            for col_name, value in key_values.items()
            if column_map.get(col_name, None) is not None
        ]

        stmt = f"""
        INSERT INTO {self.table.name}
        ({",".join(col_names)})
        VALUES
        ({",".join(col_values)}) 
        ;
        """
        return textwrap.dedent(stmt)

    def update(self, key_values: dict[str, any]):
        if not key_values:
            return ""

        column_map = {c.name: c for c in self.table.columns}
        new_values = [
            f"{k} = {SqlComposerPg.to_expr(column_map[k], value)}"
            for k, value in key_values.items()
            if column_map.get(k, None) is not None
        ]
        stmt = f"""
            UPDATE {self.table.name}
            SET {", ".join(new_values)}
            ;
        """
        return textwrap.dedent(stmt)
        

    def delete(self):
        stmt = f"""
            DELETE FROM {self.table.name}
            ;
        """
        return textwrap.dedent(stmt)

    @staticmethod
    def to_expr(column: Column, value: any) -> str:
        match column.type_:
            case PgDataTypes.TEXT | PgDataTypes.VARCHAR | PgDataTypes.CHAR | PgDataTypes.CHARACTER_VARYING:
                return f"'{value}'"
            case PgDataTypes.INT | PgDataTypes.INT4 | PgDataTypes.INTEGER:
                return str(value)
            case PgDataTypes.BIGINT | PgDataTypes.INT8:
                return str(value)
            case PgDataTypes.SMALLINT | PgDataTypes.INT2:
                return str(value)
            case PgDataTypes.NUMERIC | PgDataTypes.DECIMAL:
                return str(value)
            case PgDataTypes.REAL | PgDataTypes.FLOAT4:
                return str(value)
            case PgDataTypes.DOUBLE_PRECISION | PgDataTypes.FLOAT8:
                return str(value)
            case PgDataTypes.BOOLEAN | PgDataTypes.BOOL:
                return str(value).lower()
            case PgDataTypes.DATE:
                return f"'{value}'"
            case PgDataTypes.TIMESTAMP | PgDataTypes.TIMESTAMP_WITHOUT_TIME_ZONE:
                return f"'{value}'"
            case PgDataTypes.TIMESTAMPTZ | PgDataTypes.TIMESTAMP_WITH_TIME_ZONE:
                return f"'{value}'"
            case PgDataTypes.TIME:
                return f"'{value}'"
            case PgDataTypes.JSON | PgDataTypes.JSONB:
                return f"'{value}'"
            case PgDataTypes.UUID:
                return f"'{value}'"
            case _:
                # Default case: treat as string
                return f"'{value}'"


