from dataclasses import dataclass
from typing import List
from abc import ABC
import textwrap
from enum import Enum


class PgDataTypes(Enum):
    # String types
    TEXT = "text"
    VARCHAR = "varchar"
    CHAR = "char"
    CHARACTER_VARYING = "character varying"
    
    # Integer types
    INT = "int"
    INT4 = "int4"
    INTEGER = "integer"
    BIGINT = "bigint"
    INT8 = "int8"
    SMALLINT = "smallint"
    INT2 = "int2"
    
    # Numeric types
    NUMERIC = "numeric"
    DECIMAL = "decimal"
    REAL = "real"
    FLOAT4 = "float4"
    DOUBLE_PRECISION = "double precision"
    FLOAT8 = "float8"
    
    # Boolean types
    BOOLEAN = "boolean"
    BOOL = "bool"
    
    # Date/Time types
    DATE = "date"
    TIMESTAMP = "timestamp"
    TIMESTAMP_WITHOUT_TIME_ZONE = "timestamp without time zone"
    TIMESTAMPTZ = "timestamptz"
    TIMESTAMP_WITH_TIME_ZONE = "timestamp with time zone"
    TIME = "time"
    
    # JSON types
    JSON = "json"
    JSONB = "jsonb"
    
    # UUID type
    UUID = "uuid"


@dataclass
class Column:
    name: str
    type_: PgDataTypes


class Table(ABC):
    name: str
    columns: List[Column] = []

    def __init__(self, name: str):
        self.name = name
        self.columns = [
            value
            for name, value in vars(self.__class__).items()
            if isinstance(value, Column)
        ]


class SandboxTable(Table):
    some_str_field = Column(name="some_str_field", type_=PgDataTypes.TEXT)
    some_int_field = Column(name="some_int_field", type_=PgDataTypes.INT4)
    
    # Additional columns for key_values_2 - one from each logic path
    text_field = Column(name="text_field", type_=PgDataTypes.TEXT)
    int_field = Column(name="int_field", type_=PgDataTypes.INT)
    bigint_field = Column(name="bigint_field", type_=PgDataTypes.BIGINT)
    smallint_field = Column(name="smallint_field", type_=PgDataTypes.SMALLINT)
    numeric_field = Column(name="numeric_field", type_=PgDataTypes.NUMERIC)
    real_field = Column(name="real_field", type_=PgDataTypes.REAL)
    double_field = Column(name="double_field", type_=PgDataTypes.DOUBLE_PRECISION)
    boolean_field = Column(name="boolean_field", type_=PgDataTypes.BOOLEAN)
    date_field = Column(name="date_field", type_=PgDataTypes.DATE)
    timestamp_field = Column(name="timestamp_field", type_=PgDataTypes.TIMESTAMP)
    timestamptz_field = Column(name="timestamptz_field", type_=PgDataTypes.TIMESTAMPTZ)
    time_field = Column(name="time_field", type_=PgDataTypes.TIME)
    json_field = Column(name="json_field", type_=PgDataTypes.JSON)
    uuid_field = Column(name="uuid_field", type_=PgDataTypes.UUID)
    

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


if __name__ == "__main__":
    table = SandboxTable("some_test_table")
    sql_composer = SqlComposerPg(table)

    print(f"{sql_composer.table.name}")
    for c in sql_composer.table.columns:
        print(f"{c.name} - {c.type_}")

    print("--------------------------------SELECT--------------------------------")
    print(f"select stmt_1: {sql_composer.select()}")
    print(f"select stmt_2: {sql_composer.select(columns=[table.some_int_field])}")
    print(f"select stmt_3: {sql_composer.select(alias='alias_1')}")
    print("--------------------------------INSERT--------------------------------")
    key_values_1: dict[str, any] = {
        "some_str_field": "some_str_value",
        "some_int_field": 123,
    }
    print(f"insert stmt_1: {sql_composer.insert(key_values_1)}")
    key_values_2: dict[str, any] = {
        "text_field": "sample text value",
        "int_field": 42,
        "bigint_field": 9223372036854775807,
        "smallint_field": 32767,
        "numeric_field": 123.45,
        "real_field": 3.14,
        "double_field": 2.718281828459045,
        "boolean_field": True,
        "date_field": "2024-01-15",
        "timestamp_field": "2024-01-15 10:30:00",
        "timestamptz_field": "2024-01-15 10:30:00+00",
        "time_field": "10:30:00",
        "json_field": '{"key": "value", "number": 42}',
        "uuid_field": "550e8400-e29b-41d4-a716-446655440000",
    }
    print(f"insert stmt_2: {sql_composer.insert(key_values_2)}")
    key_values_3: dict[str, any] = {
        # String edge cases
        "text_field": "O'Connor's data with 'quotes' and \"double quotes\"", # TODO: Escape all single and double quotes
        # Numeric edge cases
        "int_field": 0,  # Zero value
        "numeric_field": float('inf'),  # Infinity
        # Boolean edge cases
        "boolean_field": False,  # False boolean
        # Date edge cases
        "date_field": "2024-02-29",  # Leap year date
        # JSON edge cases
        "json_field": '{"nested": {"array": [1, 2, 3], "null_value": null, "boolean": true, "string": "with \'quotes\'"}}',
        # UUID edge cases
        "uuid_field": "00000000-0000-0000-0000-000000000000",  # Nil UUID
    }
    print(f"insert stmt_3: {sql_composer.insert(key_values_3)}")
    print("--------------------------------UPDATE--------------------------------")
    update_values_1: dict[str, any] = {
        "some_str_field": "updated_str_value",
        "some_int_field": 456,
    }
    print(f"update stmt_1: {sql_composer.update(update_values_1)}")
    update_values_2: dict[str, any] = {
        "text_field": "updated text value",
        "int_field": 100,
        "boolean_field": False,
        "numeric_field": 999.99,
    }
    print(f"update stmt_2: {sql_composer.update(update_values_2)}")
    update_values_3: dict[str, any] = {
        # Edge cases for update
        "text_field": "Updated with 'quotes' and \"double quotes\"",
        "int_field": 0,
        "boolean_field": True,
        "date_field": "2024-12-31",
        "json_field": '{"updated": true, "timestamp": "2024-01-15T10:30:00Z"}',
    }
    print(f"update stmt_3: {sql_composer.update(update_values_3)}")
    # Test empty update
    print(f"update stmt_empty: {sql_composer.update({})}")
