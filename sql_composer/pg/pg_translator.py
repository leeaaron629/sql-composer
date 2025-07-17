from typing import Any
from sql_composer.db_models import Column, PgDataTypes
from sql_composer.db_conditions import Where, Sort, Page
from sql_composer.pg.pg_filter_op import PgFilterOp


class PgSqlTranslor:
    def val_to_sql(self, column: Column, value: Any) -> str:
        match column.type_:
            case (
                PgDataTypes.TEXT
                | PgDataTypes.VARCHAR
                | PgDataTypes.CHAR
                | PgDataTypes.CHARACTER_VARYING
            ):
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

    def where_to_sql(self, where: Where, column: Column) -> str:
        # Convert all values to SQL expressions
        values_as_pg_sql = [self.val_to_sql(column, value) for value in where.values]

        if len(values_as_pg_sql) != 1 and where.op in (
            PgFilterOp.EQUAL,
            PgFilterOp.NOT_EQUAL,
            PgFilterOp.LESS_THAN,
            PgFilterOp.LESS_THAN_OR_EQUAL,
            PgFilterOp.GREATER_THAN,
            PgFilterOp.GREATER_THAN_OR_EQUAL,
            PgFilterOp.LIKE,
            PgFilterOp.NOT_LIKE,
            PgFilterOp.ILIKE,
            PgFilterOp.NOT_ILIKE,
            PgFilterOp.REGEXP,
            PgFilterOp.NOT_REGEXP,
            PgFilterOp.REGEXP_CASE_INSENSITIVE,
            PgFilterOp.NOT_REGEXP_CASE_INSENSITIVE,
            PgFilterOp.CONTAINS,
            PgFilterOp.IS_CONTAINED_BY,
            PgFilterOp.OVERLAPS,
            PgFilterOp.JSON_CONTAINS,
            PgFilterOp.JSON_IS_CONTAINED_BY,
            PgFilterOp.JSON_HAS_KEY,
            PgFilterOp.JSON_HAS_ANY_KEY,
            PgFilterOp.JSON_HAS_ALL_KEYS,
            PgFilterOp.CONTAINS_STRING,
            PgFilterOp.NOT_CONTAINS_STRING,
            PgFilterOp.CONTAINS_STRING_CASE_INSENSITIVE,
            PgFilterOp.NOT_CONTAINS_STRING_CASE_INSENSITIVE,
            PgFilterOp.SIMILAR_TO,
            PgFilterOp.NOT_SIMILAR_TO,
            PgFilterOp.OVERLAPS_GEOMETRY,
            PgFilterOp.CONTAINS_GEOMETRY,
            PgFilterOp.IS_CONTAINED_BY_GEOMETRY,
            PgFilterOp.INTERSECTS,
            PgFilterOp.CONTAINS_INET,
            PgFilterOp.IS_CONTAINED_BY_INET,
            PgFilterOp.IS_SUBNET,
            PgFilterOp.IS_SUPERNET,
            PgFilterOp.FULLTEXT_MATCH,
            PgFilterOp.FULLTEXT_QUERY,
            PgFilterOp.IS_DISTINCT_FROM,
            PgFilterOp.IS_NOT_DISTINCT_FROM,
            PgFilterOp.ANY,
            PgFilterOp.ALL,
            PgFilterOp.SOME,
            PgFilterOp.EXISTS,
            PgFilterOp.NOT_EXISTS,
        ):
            raise ValueError(
                f"Operator {where.op} requires exactly 1 value, got {len(where.values)}"
            )

        if len(values_as_pg_sql) != 2 and where.op in (
            PgFilterOp.BETWEEN,
            PgFilterOp.NOT_BETWEEN,
        ):
            raise ValueError(
                f"Operator {where.op} requires exactly 2 values, got {len(where.values)}"
            )

        match where.op:
            # Single value operators - raise exception if multiple values provided
            case PgFilterOp.EQUAL:
                return f"{where.field} = {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_EQUAL:
                return f"{where.field} != {values_as_pg_sql[0]}"
            case PgFilterOp.LESS_THAN:
                return f"{where.field} < {values_as_pg_sql[0]}"
            case PgFilterOp.LESS_THAN_OR_EQUAL:
                return f"{where.field} <= {values_as_pg_sql[0]}"
            case PgFilterOp.GREATER_THAN:
                return f"{where.field} > {values_as_pg_sql[0]}"
            case PgFilterOp.GREATER_THAN_OR_EQUAL:
                return f"{where.field} >= {values_as_pg_sql[0]}"

            # Multiple value operators - support multiple values
            case PgFilterOp.IN:
                if len(where.values) == 1:
                    return f"{where.field} = {values_as_pg_sql[0]}"
                else:
                    return f"{where.field} IN ({', '.join(values_as_pg_sql)})"
            case PgFilterOp.NOT_IN:
                if len(where.values) == 1:
                    return f"{where.field} != {values_as_pg_sql[0]}"
                else:
                    return f"{where.field} NOT IN ({', '.join(values_as_pg_sql)})"

            # No value operators
            case PgFilterOp.IS_NULL:
                return f"{where.field} IS NULL"
            case PgFilterOp.IS_NOT_NULL:
                return f"{where.field} IS NOT NULL"

            # Single value operators - pattern matching
            case PgFilterOp.LIKE:
                return f"{where.field} LIKE {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_LIKE:
                return f"{where.field} NOT LIKE {values_as_pg_sql[0]}"
            case PgFilterOp.ILIKE:
                return f"{where.field} ILIKE {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_ILIKE:
                return f"{where.field} NOT ILIKE {values_as_pg_sql[0]}"

            # Two value operators - range operators
            case PgFilterOp.BETWEEN:
                return f"{where.field} BETWEEN {values_as_pg_sql[0]} AND {values_as_pg_sql[1]}"
            case PgFilterOp.NOT_BETWEEN:
                return f"{where.field} NOT BETWEEN {values_as_pg_sql[0]} AND {values_as_pg_sql[1]}"

            # Single value operators - regular expressions
            case PgFilterOp.REGEXP:
                return f"{where.field} ~ {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_REGEXP:
                return f"{where.field} !~ {values_as_pg_sql[0]}"
            case PgFilterOp.REGEXP_CASE_INSENSITIVE:
                return f"{where.field} ~* {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_REGEXP_CASE_INSENSITIVE:
                return f"{where.field} !~* {values_as_pg_sql[0]}"

            # Single value operators - arrays
            case PgFilterOp.CONTAINS:
                return f"{where.field} @> {values_as_pg_sql[0]}"
            case PgFilterOp.IS_CONTAINED_BY:
                return f"{where.field} <@ {values_as_pg_sql[0]}"
            case PgFilterOp.OVERLAPS:
                return f"{where.field} && {values_as_pg_sql[0]}"

            # Single value operators - JSON
            case PgFilterOp.JSON_CONTAINS:
                return f"{where.field} @> {values_as_pg_sql[0]}"
            case PgFilterOp.JSON_IS_CONTAINED_BY:
                return f"{where.field} <@ {values_as_pg_sql[0]}"
            case PgFilterOp.JSON_HAS_KEY:
                return f"{where.field} ? {values_as_pg_sql[0]}"
            case PgFilterOp.JSON_HAS_ANY_KEY:
                return f"{where.field} ?| {values_as_pg_sql[0]}"
            case PgFilterOp.JSON_HAS_ALL_KEYS:
                return f"{where.field} ?& {values_as_pg_sql[0]}"

            # Single value operators - strings
            case PgFilterOp.CONTAINS_STRING:
                return f"{where.field} ~~ {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_CONTAINS_STRING:
                return f"{where.field} !~~ {values_as_pg_sql[0]}"
            case PgFilterOp.CONTAINS_STRING_CASE_INSENSITIVE:
                return f"{where.field} ~~* {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_CONTAINS_STRING_CASE_INSENSITIVE:
                return f"{where.field} !~~* {values_as_pg_sql[0]}"

            # Single value operators - similar to
            case PgFilterOp.SIMILAR_TO:
                return f"{where.field} SIMILAR TO {values_as_pg_sql[0]}"
            case PgFilterOp.NOT_SIMILAR_TO:
                return f"{where.field} NOT SIMILAR TO {values_as_pg_sql[0]}"

            # Single value operators - geometric
            case PgFilterOp.OVERLAPS_GEOMETRY:
                return f"{where.field} && {values_as_pg_sql[0]}"
            case PgFilterOp.CONTAINS_GEOMETRY:
                return f"{where.field} @> {values_as_pg_sql[0]}"
            case PgFilterOp.IS_CONTAINED_BY_GEOMETRY:
                return f"{where.field} <@ {values_as_pg_sql[0]}"
            case PgFilterOp.INTERSECTS:
                return f"{where.field} && {values_as_pg_sql[0]}"

            # Single value operators - network
            case PgFilterOp.CONTAINS_INET:
                return f"{where.field} >> {values_as_pg_sql[0]}"
            case PgFilterOp.IS_CONTAINED_BY_INET:
                return f"{where.field} << {values_as_pg_sql[0]}"
            case PgFilterOp.IS_SUBNET:
                return f"{where.field} >>= {values_as_pg_sql[0]}"
            case PgFilterOp.IS_SUPERNET:
                return f"{where.field} <<= {values_as_pg_sql[0]}"

            # Single value operators - full text search
            case PgFilterOp.FULLTEXT_MATCH:
                return f"{where.field} @@ {values_as_pg_sql[0]}"
            case PgFilterOp.FULLTEXT_QUERY:
                return f"{where.field} @@@ {values_as_pg_sql[0]}"

            # Single value operators - special comparison
            case PgFilterOp.IS_DISTINCT_FROM:
                return f"{where.field} IS DISTINCT FROM {values_as_pg_sql[0]}"
            case PgFilterOp.IS_NOT_DISTINCT_FROM:
                return f"{where.field} IS NOT DISTINCT FROM {values_as_pg_sql[0]}"

            # Single value operators - subquery
            case PgFilterOp.ANY:
                return f"{where.field} = ANY({values_as_pg_sql[0]})"
            case PgFilterOp.ALL:
                return f"{where.field} = ALL({values_as_pg_sql[0]})"
            case PgFilterOp.SOME:
                return f"{where.field} = SOME({values_as_pg_sql[0]})"

            # Single value operators - exists
            case PgFilterOp.EXISTS:
                return f"EXISTS({values_as_pg_sql[0]})"
            case PgFilterOp.NOT_EXISTS:
                return f"NOT EXISTS({values_as_pg_sql[0]})"

            # Default case for any unhandled operators
            case _:
                raise ValueError(
                    f"Unsupported operator: {where.op} for field {where.field}"
                )

    def sort_to_sql(self, sort: Sort) -> str:
        return f"{sort.field} {sort.sort_type.value}"

    def pagination_to_sql(self, pagination: Page) -> str:
        return f"LIMIT {pagination.limit} OFFSET {pagination.offset}"
