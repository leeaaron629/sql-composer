from abc import ABC, abstractmethod
from sql_composer.db_models import Column, Sort, Page
from sql_composer.db_conditions import Where

class SqlTranslor(ABC):

    @abstractmethod
    def val_to_sql(column: Column, value: any) -> str:
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
        