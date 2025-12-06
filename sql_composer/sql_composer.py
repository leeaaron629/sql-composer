from typing import List, Any, Tuple
from sql_composer.db_models import Table, Column
import textwrap
from sql_composer.sql_translator import SqlTranslator
from sql_composer.db_conditions import WhereClause, SqlQueryCriteria

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
        self,
        columns: List[Column] | None = None,
        alias: str | None = None,
        query_criteria: SqlQueryCriteria | None = None,
    ) -> str:

        if columns is None:
            columns_by_name = {c.name: c for c in self.table.columns}
        else:
            columns_by_name = {c.name: c for c in columns}

        col_names = columns_by_name.keys()
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
        {self.translator.query_criteria_to_sql(query_criteria, self.table)}
        """

        return textwrap.dedent(stmt)

    def select_with_params(
        self,
        columns: List[Column] | None = None,
        alias: str | None = None,
        query_criteria: SqlQueryCriteria | None = None,
    ) -> Tuple[str, List[Any]]:
        """
        Generate a parameterized SELECT query.
        Returns a tuple of (SQL, parameters) for safe execution.
        """
        if columns is None:
            columns_by_name = {c.name: c for c in self.table.columns}
        else:
            columns_by_name = {c.name: c for c in columns}

        col_names = columns_by_name.keys()
        if alias is None:
            table_name = self.table.name
            col_names_fmted = ", ".join(col_names)
        else:
            table_name = f"{self.table.name} AS {alias}"
            col_names_fmted = ", ".join([f"{alias}.{c_name}" for c_name in col_names])

        # Generate parameterized SQL and extract parameters
        sql, params = self.translator.query_criteria_to_sql_with_params(query_criteria, self.table)

        stmt = f"""
        SELECT
            {col_names_fmted}
        FROM {table_name}
        {sql}
        """

        return textwrap.dedent(stmt), params

    def insert(self, key_values: dict[str, Any]):
        column_map = {c.name: c for c in self.table.columns}

        col_names = [k for k in key_values.keys() if column_map.get(k, None) is not None]
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

    def insert_with_params(self, key_values: dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        Generate a parameterized INSERT query.
        Returns a tuple of (SQL, parameters) for safe execution.
        """
        column_map = {c.name: c for c in self.table.columns}

        # Filter to only include valid columns
        valid_key_values = {k: v for k, v in key_values.items() if column_map.get(k, None) is not None}

        if not valid_key_values:
            return "", []

        col_names = list(valid_key_values.keys())
        col_values = list(valid_key_values.values())

        # Create parameter placeholders
        placeholders = ", ".join(["%s"] * len(col_values))

        stmt = f"""
        INSERT INTO {self.table.name}
        ({",".join(col_names)})
        VALUES
        ({placeholders})
        ;
        """

        return textwrap.dedent(stmt), col_values

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

    def update_with_params(self, key_values: dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        Generate a parameterized UPDATE query.
        Returns a tuple of (SQL, parameters) for safe execution.
        """
        if not key_values:
            return "", []

        column_map = {c.name: c for c in self.table.columns}

        # Filter to only include valid columns
        valid_key_values = {k: v for k, v in key_values.items() if column_map.get(k, None) is not None}

        if not valid_key_values:
            return "", []

        # Create SET clause with parameter placeholders
        set_clauses = [f"{k} = %s" for k in valid_key_values.keys()]
        values = list(valid_key_values.values())

        stmt = f"""
            UPDATE {self.table.name}
            SET {", ".join(set_clauses)}
            ;
        """

        return textwrap.dedent(stmt), values

    def delete(self):
        stmt = f"""
            DELETE FROM {self.table.name}
            ;
        """
        return textwrap.dedent(stmt)
