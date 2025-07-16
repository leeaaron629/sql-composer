from enum import Enum
from typing import List
from sql_composer.db_models import Table

class FilterOp(Enum):
    # Comparison operators
    EQUAL = "="
    NOT_EQUAL = "!="
    NOT_EQUAL_ALT = "<>"
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    
    # Pattern matching operators
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"
    ILIKE = "ILIKE"
    NOT_ILIKE = "NOT ILIKE"
    SIMILAR_TO = "SIMILAR TO"
    NOT_SIMILAR_TO = "NOT SIMILAR TO"
    REGEXP = "~"
    NOT_REGEXP = "!~"
    REGEXP_CASE_INSENSITIVE = "~*"
    NOT_REGEXP_CASE_INSENSITIVE = "!~*"
    
    # Set membership operators
    IN = "IN"
    NOT_IN = "NOT IN"
    
    # Null operators
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    
    # Range operators
    BETWEEN = "BETWEEN"
    NOT_BETWEEN = "NOT BETWEEN"
    
    # Array operators
    CONTAINS = "@>"
    IS_CONTAINED_BY = "<@"
    OVERLAPS = "&&"
    
    # JSON operators
    JSON_CONTAINS = "@>"
    JSON_IS_CONTAINED_BY = "<@"
    JSON_HAS_KEY = "?"
    JSON_HAS_ANY_KEY = "?|"
    JSON_HAS_ALL_KEYS = "?&"
    
    # Logical operators
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Exists operators
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT EXISTS"
    
    # Subquery operators
    ANY = "ANY"
    ALL = "ALL"
    SOME = "SOME"
    
    # String operators
    CONCATENATE = "||"
    CONTAINS_STRING = "~~"
    NOT_CONTAINS_STRING = "!~~"
    CONTAINS_STRING_CASE_INSENSITIVE = "~~*"
    NOT_CONTAINS_STRING_CASE_INSENSITIVE = "!~~*"
    
    # Bitwise operators
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_XOR = "#"
    BITWISE_NOT = "~"
    BITWISE_LEFT_SHIFT = "<<"
    BITWISE_RIGHT_SHIFT = ">>"
    
    # Mathematical operators
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "^"
    ABSOLUTE_VALUE = "@"
    SQUARE_ROOT = "|/"
    CUBE_ROOT = "||/"
    
    # Geometric operators
    OVERLAPS_GEOMETRY = "&&"
    CONTAINS_GEOMETRY = "@>"
    IS_CONTAINED_BY_GEOMETRY = "<@"
    INTERSECTS = "&&"
    
    # Network operators
    CONTAINS_INET = ">>"
    IS_CONTAINED_BY_INET = "<<"
    IS_SUBNET = ">>="
    IS_SUPERNET = "<<="
    
    # Full text search operators
    FULLTEXT_MATCH = "@@"
    FULLTEXT_QUERY = "@@@"
    
    # Custom operators (less common but available)
    IS_DISTINCT_FROM = "IS DISTINCT FROM"
    IS_NOT_DISTINCT_FROM = "IS NOT DISTINCT FROM"

class Where:
    
    def __init__(self, field: str, op: FilterOp, values: List[any]):
        self.field = field
        self.op = op
        self.values = values

class WhereClause:
    
    def __init__(self, conditions: List[Where]):
        self.conditions = conditions

    @staticmethod
    def to_expr(conditions: List[Where], table: Table) -> str:
        exprs = []
        for condition in conditions:
            match condition.op:
                case FilterOp.EQUAL, FilterOp.IN:
                    if len(condition.values) > 1:
                        exprs.append(f"{condition.field} IN ({', '.join(condition.values)})")
                    else:
                        exprs.append(f"{condition.field} = {condition.values[0]}")
                case FilterOp.NOT_EQUAL, FilterOp.NOT_IN:
                    if len(condition.values) > 1:
                        exprs.append(f"{condition.field} NOT IN ({', '.join(condition.values)})")
                
        return " AND ".join(exprs)

    

