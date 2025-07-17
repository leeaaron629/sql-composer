from abc import ABC, abstractmethod
from typing import Any
from sql_composer.db_models import Column
from sql_composer.db_conditions import Where, Sort, Page


class SqlTranslator(ABC):
    @abstractmethod
    def val_to_sql(self, column: Column, value: Any) -> str:
        pass

    @abstractmethod
    def where_to_sql(self, where: Where, column: Column) -> str:
        pass

    @abstractmethod
    def sort_to_sql(self, sort: Sort) -> str:
        pass

    @abstractmethod
    def pagination_to_sql(self, pagination: Page) -> str:
        pass
