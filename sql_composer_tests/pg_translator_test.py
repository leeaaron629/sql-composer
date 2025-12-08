import unittest
from sql_composer.pg.pg_translator import PgSqlTranslator
from sql_composer.db_models import Column, Table
from sql_composer.db_conditions import Where, WhereClause, Sort, Page, SqlQueryCriteria, SortType
from sql_composer.pg.pg_data_types import PgDataTypes
from sql_composer.pg.pg_filter_op import PgFilterOp


class MockTable(Table):
    """Mock table for query_criteria_to_sql tests"""

    username = Column("name", PgDataTypes.TEXT)
    age = Column("age", PgDataTypes.INT)
    created_at = Column("created_at", PgDataTypes.TIMESTAMP)


class TestPgSqlTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = PgSqlTranslator()
        self.test_table = MockTable("test_table")

    def test_val_to_sql_string_types(self):
        """Test val_to_sql for string data types"""
        text_col = Column("name", PgDataTypes.TEXT)
        varchar_col = Column("code", PgDataTypes.VARCHAR)

        self.assertEqual(self.translator.val_to_sql(text_col, "test"), "'test'")
        self.assertEqual(self.translator.val_to_sql(varchar_col, "ABC123"), "'ABC123'")

    def test_val_to_sql_numeric_types(self):
        """Test val_to_sql for numeric data types"""
        int_col = Column("id", PgDataTypes.INT)
        bigint_col = Column("count", PgDataTypes.BIGINT)
        numeric_col = Column("price", PgDataTypes.NUMERIC)

        self.assertEqual(self.translator.val_to_sql(int_col, 42), "42")
        self.assertEqual(self.translator.val_to_sql(bigint_col, 9223372036854775807), "9223372036854775807")
        self.assertEqual(self.translator.val_to_sql(numeric_col, 123.45), "123.45")

    def test_val_to_sql_special_float_values(self):
        """Test val_to_sql for special float values (infinity, -infinity, NaN)"""
        numeric_col = Column("value", PgDataTypes.NUMERIC)
        decimal_col = Column("amount", PgDataTypes.DECIMAL)
        real_col = Column("rate", PgDataTypes.REAL)
        double_col = Column("precision", PgDataTypes.DOUBLE_PRECISION)

        # Test positive infinity
        self.assertEqual(self.translator.val_to_sql(numeric_col, float("inf")), "'Infinity'")
        self.assertEqual(self.translator.val_to_sql(decimal_col, float("inf")), "'Infinity'")
        self.assertEqual(self.translator.val_to_sql(real_col, float("inf")), "'Infinity'")
        self.assertEqual(self.translator.val_to_sql(double_col, float("inf")), "'Infinity'")

        # Test negative infinity
        self.assertEqual(self.translator.val_to_sql(numeric_col, float("-inf")), "'-Infinity'")
        self.assertEqual(self.translator.val_to_sql(decimal_col, float("-inf")), "'-Infinity'")
        self.assertEqual(self.translator.val_to_sql(real_col, float("-inf")), "'-Infinity'")
        self.assertEqual(self.translator.val_to_sql(double_col, float("-inf")), "'-Infinity'")

        # Test NaN
        self.assertEqual(self.translator.val_to_sql(numeric_col, float("nan")), "'NaN'")
        self.assertEqual(self.translator.val_to_sql(decimal_col, float("nan")), "'NaN'")
        self.assertEqual(self.translator.val_to_sql(real_col, float("nan")), "'NaN'")
        self.assertEqual(self.translator.val_to_sql(double_col, float("nan")), "'NaN'")

    def test_val_to_sql_boolean_types(self):
        """Test val_to_sql for boolean data types"""
        bool_col = Column("active", PgDataTypes.BOOLEAN)

        self.assertEqual(self.translator.val_to_sql(bool_col, True), "true")
        self.assertEqual(self.translator.val_to_sql(bool_col, False), "false")

    def test_val_to_sql_date_time_types(self):
        """Test val_to_sql for date/time data types"""
        date_col = Column("created_at", PgDataTypes.DATE)
        timestamp_col = Column("updated_at", PgDataTypes.TIMESTAMP)

        self.assertEqual(self.translator.val_to_sql(date_col, "2024-01-15"), "'2024-01-15'")
        self.assertEqual(self.translator.val_to_sql(timestamp_col, "2024-01-15 10:30:00"), "'2024-01-15 10:30:00'")

    def test_val_to_sql_json_uuid_types(self):
        """Test val_to_sql for JSON and UUID data types"""
        json_col = Column("data", PgDataTypes.JSON)
        uuid_col = Column("id", PgDataTypes.UUID)

        self.assertEqual(self.translator.val_to_sql(json_col, '{"key": "value"}'), '\'{"key": "value"}\'')
        self.assertEqual(
            self.translator.val_to_sql(uuid_col, "550e8400-e29b-41d4-a716-446655440000"),
            "'550e8400-e29b-41d4-a716-446655440000'",
        )

    def test_where_to_sql_single_value_operators(self):
        """Test where_to_sql for single value operators"""
        column = Column("name", PgDataTypes.TEXT)

        # Test EQUAL
        where = Where("name", PgFilterOp.EQUAL, ["John"])
        self.assertEqual(self.translator.where_to_sql(where, column), "name = 'John'")

        # Test GREATER_THAN
        int_column = Column("age", PgDataTypes.INT)
        where = Where("age", PgFilterOp.GREATER_THAN, [25])
        self.assertEqual(self.translator.where_to_sql(where, int_column), "age > 25")

    def test_where_to_sql_multiple_value_operators(self):
        """Test where_to_sql for multiple value operators"""
        column = Column("status", PgDataTypes.TEXT)

        # Test IN with multiple values
        where = Where("status", PgFilterOp.IN, ["active", "pending", "completed"])
        self.assertEqual(self.translator.where_to_sql(where, column), "status IN ('active', 'pending', 'completed')")

        # Test IN with single value (should convert to EQUAL)
        where = Where("status", PgFilterOp.IN, ["active"])
        self.assertEqual(self.translator.where_to_sql(where, column), "status = 'active'")

    def test_where_to_sql_no_value_operators(self):
        """Test where_to_sql for no value operators"""
        column = Column("name", PgDataTypes.TEXT)

        # Test IS_NULL
        where = Where("name", PgFilterOp.IS_NULL, [])
        self.assertEqual(self.translator.where_to_sql(where, column), "name IS NULL")

        # Test IS_NOT_NULL
        where = Where("name", PgFilterOp.IS_NOT_NULL, [])
        self.assertEqual(self.translator.where_to_sql(where, column), "name IS NOT NULL")

    def test_where_to_sql_two_value_operators(self):
        """Test where_to_sql for two value operators"""
        column = Column("price", PgDataTypes.NUMERIC)

        # Test BETWEEN
        where = Where("price", PgFilterOp.BETWEEN, [10.0, 100.0])
        self.assertEqual(self.translator.where_to_sql(where, column), "price BETWEEN 10.0 AND 100.0")

    def test_where_to_sql_validation_errors(self):
        """Test where_to_sql validation for incorrect number of values"""
        column = Column("name", PgDataTypes.TEXT)

        # Test EQUAL with multiple values (should raise error)
        where = Where("name", PgFilterOp.EQUAL, ["John", "Jane"])
        with self.assertRaises(ValueError) as context:
            self.translator.where_to_sql(where, column)
        self.assertIn("requires exactly 1 value", str(context.exception))

        # Test BETWEEN with single value (should raise error)
        where = Where("price", PgFilterOp.BETWEEN, [10.0])
        with self.assertRaises(ValueError) as context:
            self.translator.where_to_sql(where, column)
        self.assertIn("requires exactly 2 values", str(context.exception))

    def test_sort_to_sql(self):
        """Test sort_to_sql method"""
        sort_asc = Sort("name", SortType.ASC)
        sort_desc = Sort("created_at", SortType.DESC)

        self.assertEqual(self.translator.sort_to_sql(sort_asc), "name ASC")
        self.assertEqual(self.translator.sort_to_sql(sort_desc), "created_at DESC")

    def test_page_criteria_to_sql(self):
        """Test page_criteria_to_sql method"""
        # Test with both limit and offset
        page = Page(limit=10, offset=20)
        self.assertEqual(self.translator.page_criteria_to_sql(page), "LIMIT 10 OFFSET 20")

        # Test with only limit
        page = Page(limit=5, offset=None)
        self.assertEqual(self.translator.page_criteria_to_sql(page), "LIMIT 5")

        # Test with only offset
        page = Page(limit=None, offset=15)
        self.assertEqual(self.translator.page_criteria_to_sql(page), "OFFSET 15")

        # Test with neither
        page = Page(limit=None, offset=None)
        self.assertEqual(self.translator.page_criteria_to_sql(page), "")

    def test_query_criteria_to_sql_where_only(self):
        """Test query_criteria_to_sql with only WHERE clause"""
        where_clause = WhereClause(
            [Where("name", PgFilterOp.EQUAL, ["John"]), Where("age", PgFilterOp.GREATER_THAN, [25])]
        )

        query_criteria = SqlQueryCriteria(where=where_clause)
        result = self.translator.query_criteria_to_sql(query_criteria, self.test_table)

        self.assertIn("WHERE", result)
        self.assertIn("name = 'John'", result)
        self.assertIn("age > 25", result)
        self.assertIn("AND", result)

    def test_query_criteria_to_sql_sort_only(self):
        """Test query_criteria_to_sql with only SORT clause"""
        sort_clause = [Sort("name", SortType.ASC), Sort("created_at", SortType.DESC)]

        query_criteria = SqlQueryCriteria(sort=sort_clause)
        result = self.translator.query_criteria_to_sql(query_criteria, self.test_table)

        self.assertIn("ORDER BY", result)
        self.assertIn("name ASC", result)
        self.assertIn("created_at DESC", result)

    def test_query_criteria_to_sql_pagination_only(self):
        """Test query_criteria_to_sql with only PAGINATION clause"""
        page = Page(limit=10, offset=20)
        query_criteria = SqlQueryCriteria(page=page)
        result = self.translator.query_criteria_to_sql(query_criteria, self.test_table)

        self.assertIn("LIMIT 10", result)
        self.assertIn("OFFSET 20", result)

    def test_query_criteria_to_sql_complete(self):
        """Test query_criteria_to_sql with all clauses"""
        where_clause = WhereClause([Where("name", PgFilterOp.EQUAL, ["John"])])
        sort_clause = [Sort("age", SortType.ASC)]
        page = Page(limit=10, offset=20)

        query_criteria = SqlQueryCriteria(where=where_clause, sort=sort_clause, page=page)

        result = self.translator.query_criteria_to_sql(query_criteria, self.test_table)

        # Should contain all clauses
        self.assertIn("WHERE", result)
        self.assertIn("ORDER BY", result)
        self.assertIn("LIMIT", result)
        self.assertIn("OFFSET", result)
        self.assertIn("name = 'John'", result)
        self.assertIn("age ASC", result)

    def test_query_criteria_to_sql_unknown_field(self):
        """Test query_criteria_to_sql with unknown field (should be filtered out)"""
        where_clause = WhereClause(
            [
                Where("name", PgFilterOp.EQUAL, ["John"]),
                Where("unknown_field", PgFilterOp.EQUAL, ["value"]),  # This should be filtered out
            ]
        )

        query_criteria = SqlQueryCriteria(where=where_clause)
        result = self.translator.query_criteria_to_sql(query_criteria, self.test_table)

        # Should only contain the known field
        self.assertIn("name = 'John'", result)
        self.assertNotIn("unknown_field", result)


if __name__ == "__main__":
    unittest.main()
