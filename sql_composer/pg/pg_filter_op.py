from enum import Enum
from sql_composer.db_conditions import FilterOp


class PgFilterOp(Enum, FilterOp):
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
