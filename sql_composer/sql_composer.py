from typing import List, Any
from sql_composer.db_models import Table, Column
import textwrap
from sql_composer.sql_translator import SqlTranslator

"""
SqlComposer is a class that composes SQL statements.
It is used to compose SQL statements for a given table and a given translator.
The translator is responsible for translating the SQL statements to the appropriate SQL dialect.

Future Extension:
For cases where the SqlComposer core logic is not re-useable, 
please extend the SqlComposer class and override the methods you need.
"""
class SqlComposer:
    def __init__(self, translator: SqlTranslator, table: Table):
        self.translator = translator
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

    def insert(self, key_values: dict[str, Any]):
        column_map = {c.name: c for c in self.table.columns}

        col_names = [f"'{k}'" for k in key_values.keys()]
        col_values = [
            self.translator.val_to_sql(column_map[col_name], value)
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

    def update(self, key_values: dict[str, Any]):
        if not key_values:
            return ""

        column_map = {c.name: c for c in self.table.columns}
        new_values = [
            f"{k} = {self.translator.val_to_sql(column_map[k], value)}"
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
