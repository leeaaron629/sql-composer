from typing import List, Any
from enum import Enum
from dataclasses import dataclass


# Sort Clause
class SortType(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class Sort:
    field: str
    sort_type: SortType


# Pagination Clause
@dataclass
class Page:
    limit: int
    offset: int


# Filter Operators
class FilterOp:
    pass


@dataclass
class Where:
    field: str
    op: FilterOp
    values: List[Any]


# WHERE Clause
@dataclass
class WhereClause:
    conditions: List[Where]
