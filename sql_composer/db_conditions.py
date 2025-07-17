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
    
    # String operators
    CONTAINS_STRING = "~~"
    NOT_CONTAINS_STRING = "!~~"
    CONTAINS_STRING_CASE_INSENSITIVE = "~~*"
    NOT_CONTAINS_STRING_CASE_INSENSITIVE = "!~~*"
    
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
    
    # Special comparison operators
    IS_DISTINCT_FROM = "IS DISTINCT FROM"
    IS_NOT_DISTINCT_FROM = "IS NOT DISTINCT FROM"
    
    # Subquery operators
    ANY = "ANY"
    ALL = "ALL"
    SOME = "SOME"
    
    # Exists operators
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT EXISTS"

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
                # Most frequently used - Comparison operators
                case FilterOp.EQUAL:
                    exprs.append(f"{condition.field} = {condition.values[0]}")
                case FilterOp.NOT_EQUAL:
                    exprs.append(f"{condition.field} != {condition.values[0]}")
                case FilterOp.LESS_THAN:
                    exprs.append(f"{condition.field} < {condition.values[0]}")
                case FilterOp.LESS_THAN_OR_EQUAL:
                    exprs.append(f"{condition.field} <= {condition.values[0]}")
                case FilterOp.GREATER_THAN:
                    exprs.append(f"{condition.field} > {condition.values[0]}")
                case FilterOp.GREATER_THAN_OR_EQUAL:
                    exprs.append(f"{condition.field} >= {condition.values[0]}")
                
                # Set membership operators
                case FilterOp.IN:
                    if len(condition.values) > 1:
                        exprs.append(f"{condition.field} IN ({', '.join(map(str, condition.values))})")
                    else:
                        exprs.append(f"{condition.field} = {condition.values[0]}")
                case FilterOp.NOT_IN:
                    if len(condition.values) > 1:
                        exprs.append(f"{condition.field} NOT IN ({', '.join(map(str, condition.values))})")
                    else:
                        exprs.append(f"{condition.field} != {condition.values[0]}")
                
                # Null operators
                case FilterOp.IS_NULL:
                    exprs.append(f"{condition.field} IS NULL")
                case FilterOp.IS_NOT_NULL:
                    exprs.append(f"{condition.field} IS NOT NULL")
                
                # Pattern matching operators
                case FilterOp.LIKE:
                    exprs.append(f"{condition.field} LIKE {condition.values[0]}")
                case FilterOp.NOT_LIKE:
                    exprs.append(f"{condition.field} NOT LIKE {condition.values[0]}")
                case FilterOp.ILIKE:
                    exprs.append(f"{condition.field} ILIKE {condition.values[0]}")
                case FilterOp.NOT_ILIKE:
                    exprs.append(f"{condition.field} NOT ILIKE {condition.values[0]}")
                
                # Range operators
                case FilterOp.BETWEEN:
                    if len(condition.values) >= 2:
                        exprs.append(f"{condition.field} BETWEEN {condition.values[0]} AND {condition.values[1]}")
                case FilterOp.NOT_BETWEEN:
                    if len(condition.values) >= 2:
                        exprs.append(f"{condition.field} NOT BETWEEN {condition.values[0]} AND {condition.values[1]}")
                
                # Regular expression operators
                case FilterOp.REGEXP:
                    exprs.append(f"{condition.field} ~ {condition.values[0]}")
                case FilterOp.NOT_REGEXP:
                    exprs.append(f"{condition.field} !~ {condition.values[0]}")
                case FilterOp.REGEXP_CASE_INSENSITIVE:
                    exprs.append(f"{condition.field} ~* {condition.values[0]}")
                case FilterOp.NOT_REGEXP_CASE_INSENSITIVE:
                    exprs.append(f"{condition.field} !~* {condition.values[0]}")
                
                # Array operators
                case FilterOp.CONTAINS:
                    exprs.append(f"{condition.field} @> {condition.values[0]}")
                case FilterOp.IS_CONTAINED_BY:
                    exprs.append(f"{condition.field} <@ {condition.values[0]}")
                case FilterOp.OVERLAPS:
                    exprs.append(f"{condition.field} && {condition.values[0]}")
                
                # JSON operators
                case FilterOp.JSON_CONTAINS:
                    exprs.append(f"{condition.field} @> {condition.values[0]}")
                case FilterOp.JSON_IS_CONTAINED_BY:
                    exprs.append(f"{condition.field} <@ {condition.values[0]}")
                case FilterOp.JSON_HAS_KEY:
                    exprs.append(f"{condition.field} ? {condition.values[0]}")
                case FilterOp.JSON_HAS_ANY_KEY:
                    exprs.append(f"{condition.field} ?| {condition.values[0]}")
                case FilterOp.JSON_HAS_ALL_KEYS:
                    exprs.append(f"{condition.field} ?& {condition.values[0]}")
                
                # String operators
                case FilterOp.CONTAINS_STRING:
                    exprs.append(f"{condition.field} ~~ {condition.values[0]}")
                case FilterOp.NOT_CONTAINS_STRING:
                    exprs.append(f"{condition.field} !~~ {condition.values[0]}")
                case FilterOp.CONTAINS_STRING_CASE_INSENSITIVE:
                    exprs.append(f"{condition.field} ~~* {condition.values[0]}")
                case FilterOp.NOT_CONTAINS_STRING_CASE_INSENSITIVE:
                    exprs.append(f"{condition.field} !~~* {condition.values[0]}")
                
                # Similar to operators
                case FilterOp.SIMILAR_TO:
                    exprs.append(f"{condition.field} SIMILAR TO {condition.values[0]}")
                case FilterOp.NOT_SIMILAR_TO:
                    exprs.append(f"{condition.field} NOT SIMILAR TO {condition.values[0]}")
                
                # Geometric operators
                case FilterOp.OVERLAPS_GEOMETRY:
                    exprs.append(f"{condition.field} && {condition.values[0]}")
                case FilterOp.CONTAINS_GEOMETRY:
                    exprs.append(f"{condition.field} @> {condition.values[0]}")
                case FilterOp.IS_CONTAINED_BY_GEOMETRY:
                    exprs.append(f"{condition.field} <@ {condition.values[0]}")
                case FilterOp.INTERSECTS:
                    exprs.append(f"{condition.field} && {condition.values[0]}")
                
                # Network operators
                case FilterOp.CONTAINS_INET:
                    exprs.append(f"{condition.field} >> {condition.values[0]}")
                case FilterOp.IS_CONTAINED_BY_INET:
                    exprs.append(f"{condition.field} << {condition.values[0]}")
                case FilterOp.IS_SUBNET:
                    exprs.append(f"{condition.field} >>= {condition.values[0]}")
                case FilterOp.IS_SUPERNET:
                    exprs.append(f"{condition.field} <<= {condition.values[0]}")
                
                # Full text search operators
                case FilterOp.FULLTEXT_MATCH:
                    exprs.append(f"{condition.field} @@ {condition.values[0]}")
                case FilterOp.FULLTEXT_QUERY:
                    exprs.append(f"{condition.field} @@@ {condition.values[0]}")
                
                # Special comparison operators
                case FilterOp.IS_DISTINCT_FROM:
                    exprs.append(f"{condition.field} IS DISTINCT FROM {condition.values[0]}")
                case FilterOp.IS_NOT_DISTINCT_FROM:
                    exprs.append(f"{condition.field} IS NOT DISTINCT FROM {condition.values[0]}")
                
                # Subquery operators
                case FilterOp.ANY:
                    exprs.append(f"{condition.field} = ANY({condition.values[0]})")
                case FilterOp.ALL:
                    exprs.append(f"{condition.field} = ALL({condition.values[0]})")
                case FilterOp.SOME:
                    exprs.append(f"{condition.field} = SOME({condition.values[0]})")
                
                # Exists operators (typically used with subqueries)
                case FilterOp.EXISTS:
                    exprs.append(f"EXISTS({condition.values[0]})")
                case FilterOp.NOT_EXISTS:
                    exprs.append(f"NOT EXISTS({condition.values[0]})")
                
                # Default case for any unhandled operators
                case _:
                    exprs.append(f"{condition.field} {condition.op.value} {condition.values[0] if condition.values else ''}")
                                
        return " AND ".join(exprs)

    

