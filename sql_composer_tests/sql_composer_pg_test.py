from sql_composer.db_models import Table, Column, PgDataTypes
from sql_composer.sql_composer_pg import SqlComposerPg


class SandboxTable(Table):
    some_str_field = Column(name="some_str_field", type_=PgDataTypes.TEXT)
    some_int_field = Column(name="some_int_field", type_=PgDataTypes.INT4)

    # Additional columns for key_values_2 - one from each logic path
    text_field = Column(name="text_field", type_=PgDataTypes.TEXT)
    int_field = Column(name="int_field", type_=PgDataTypes.INT)
    bigint_field = Column(name="bigint_field", type_=PgDataTypes.BIGINT)
    smallint_field = Column(name="smallint_field", type_=PgDataTypes.SMALLINT)
    numeric_field = Column(name="numeric_field", type_=PgDataTypes.NUMERIC)
    real_field = Column(name="real_field", type_=PgDataTypes.REAL)
    double_field = Column(name="double_field", type_=PgDataTypes.DOUBLE_PRECISION)
    boolean_field = Column(name="boolean_field", type_=PgDataTypes.BOOLEAN)
    date_field = Column(name="date_field", type_=PgDataTypes.DATE)
    timestamp_field = Column(name="timestamp_field", type_=PgDataTypes.TIMESTAMP)
    timestamptz_field = Column(name="timestamptz_field", type_=PgDataTypes.TIMESTAMPTZ)
    time_field = Column(name="time_field", type_=PgDataTypes.TIME)
    json_field = Column(name="json_field", type_=PgDataTypes.JSON)
    uuid_field = Column(name="uuid_field", type_=PgDataTypes.UUID)


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
    key_values_1: dict[str, any] = {
        "some_str_field": "some_str_value",
        "some_int_field": 123,
    }
    print(f"insert stmt_1: {sql_composer.insert(key_values_1)}")
    key_values_2: dict[str, any] = {
        "text_field": "sample text value",
        "int_field": 42,
        "bigint_field": 9223372036854775807,
        "smallint_field": 32767,
        "numeric_field": 123.45,
        "real_field": 3.14,
        "double_field": 2.718281828459045,
        "boolean_field": True,
        "date_field": "2024-01-15",
        "timestamp_field": "2024-01-15 10:30:00",
        "timestamptz_field": "2024-01-15 10:30:00+00",
        "time_field": "10:30:00",
        "json_field": '{"key": "value", "number": 42}',
        "uuid_field": "550e8400-e29b-41d4-a716-446655440000",
    }
    print(f"insert stmt_2: {sql_composer.insert(key_values_2)}")
    key_values_3: dict[str, any] = {
        # String edge cases
        "text_field": "O'Connor's data with 'quotes' and \"double quotes\"",  # TODO: Escape all single and double quotes
        # Numeric edge cases
        "int_field": 0,  # Zero value
        "numeric_field": float("inf"),  # Infinity
        # Boolean edge cases
        "boolean_field": False,  # False boolean
        # Date edge cases
        "date_field": "2024-02-29",  # Leap year date
        # JSON edge cases
        "json_field": '{"nested": {"array": [1, 2, 3], "null_value": null, "boolean": true, "string": "with \'quotes\'"}}',
        # UUID edge cases
        "uuid_field": "00000000-0000-0000-0000-000000000000",  # Nil UUID
    }
    print(f"insert stmt_3: {sql_composer.insert(key_values_3)}")
    print("--------------------------------UPDATE--------------------------------")
    update_values_1: dict[str, any] = {
        "some_str_field": "updated_str_value",
        "some_int_field": 456,
    }
    print(f"update stmt_1: {sql_composer.update(update_values_1)}")
    update_values_2: dict[str, any] = {
        "text_field": "updated text value",
        "int_field": 100,
        "boolean_field": False,
        "numeric_field": 999.99,
    }
    print(f"update stmt_2: {sql_composer.update(update_values_2)}")
    update_values_3: dict[str, any] = {
        # Edge cases for update
        "text_field": "Updated with 'quotes' and \"double quotes\"",
        "int_field": 0,
        "boolean_field": True,
        "date_field": "2024-12-31",
        "json_field": '{"updated": true, "timestamp": "2024-01-15T10:30:00Z"}',
    }
    print(f"update stmt_3: {sql_composer.update(update_values_3)}")
    # Test empty update
    print(f"update stmt_empty: {sql_composer.update({})}")
