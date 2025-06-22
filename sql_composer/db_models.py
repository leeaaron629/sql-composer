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
        FROM {self.table.name}
        ;
        """

        return textwrap.dedent(stmt)

    def insert(self, key_values: dict[str, any]):
        column_map = {c.name: c for c in self.table.columns}

        col_names_fmted = ", ".join([f"'{k}'" for k in key_values.keys()])
        col_values_fmted = ", ".join(
            [
                SqlComposerPg.to_expr(column_map[col_name], value)
                for col_name, value in key_values.items()
                if column_map.get(col_name, None) is not None
            ]
        )  # TODO: Map value to the right SQL stmt based on column data type

        stmt = f"""
        INSERT INTO {self.table.name}
        ({col_names_fmted})
        VALUES
        ({col_values_fmted}) 
        ;
        """
        return textwrap.dedent(stmt)

    def update(self):
        pass

    def delete(self):
        pass

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
    key_values: dict[str, any] = {
        "some_str_field": "some_str_value",
        "some_int_field": 123,
    }
    print(f"insert stmt_1: {sql_composer.insert(key_values)}")
