from dataclasses import dataclass
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional, List
from abc import ABC, abstractmethod
import textwrap


@dataclass
class Column:
    name: str
    data_type: str


class Table(ABC):
    name: str
    columns: List[Column] = []

    def __init__(self, name: str):
        self.name = name
        self.columns = [
            value for name, value in vars(self.__class__).items()
            if isinstance(value, Column)
        ]

class SandboxTable(Table):

    some_str_field = Column(name="some_str_field", data_type="text")
    some_int_field = Column(name="some_int_field", data_type="int4")

class SqlComposerPg:

    def __init__(self, table: Table):
        self.table = table

    def select(self, columns: List[Column] | None = None, alias: str | None = None) -> str:
    
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
        col_names_fmted = ", ".join([f"'{k}'" for k in key_values.keys()])
        col_values_fmted = ", ".join([f"'{v}'" for v in key_values.values()])

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


if __name__ == "__main__":
    table = SandboxTable("some_test_table")
    sql_composer = SqlComposerPg(table)

    print(f"{sql_composer.table.name}")
    for c in sql_composer.table.columns:
        print(f"{c.name} - {c.data_type}")

    print("--------------------------------SELECT--------------------------------")
    print(f"select stmt_1: {sql_composer.select()}")
    print(f"select stmt_2: {sql_composer.select(columns=[table.some_int_field])}")
    print(f"select stmt_3: {sql_composer.select(alias='alias_1')}")
    print("--------------------------------INSERT--------------------------------")
    key_values: dict[str, any] = {
        "some_str_field": "some_str_value",
        "some_int_field": 123
    }
    print(f"insert stmt_1: {sql_composer.insert(key_values)}")



    