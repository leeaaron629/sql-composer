# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

This project uses `uv` as the package manager and build tool. All commands are available through the Makefile.

### Setup
```bash
make install          # Install dependencies using uv
```

### Testing
```bash
make test            # Run all tests with coverage
uv run python -m pytest sql_composer_tests/ -k <test_name>  # Run specific test
uv run python -m pytest sql_composer_tests/<test_file>.py  # Run specific test file
```

### Linting and Formatting
```bash
make lint            # Run ruff and pyright linters
make format          # Format code with ruff and auto-fix issues
uv run python -m ruff check .       # Run ruff linter only
uv run python -m pyright            # Run type checker only
```

### Building
```bash
make build           # Build the package
```

### Cleanup
```bash
make clean           # Remove cache files and build artifacts
```

## Architecture Overview

### Core Abstractions

**sql-composer** is a SQL query builder library that separates query composition logic from database-specific translation. The architecture follows a translator pattern:

1. **SqlComposer** (`sql_composer.py`): Core query builder that generates SQL statements (SELECT, INSERT, UPDATE, DELETE). It delegates database-specific syntax to translators.

2. **SqlTranslator** (`sql_translator.py`): Abstract base class defining the interface for database-specific translators. Concrete implementations handle dialect differences.

3. **Table and Column Models** (`db_models.py`): Define database schema. Tables inherit from `Table` abstract class and declare columns as class attributes. Column types are enums (e.g., `PgDataTypes`).

4. **Query Conditions** (`db_conditions.py`): Data classes for query filtering:
   - `WhereClause`: Contains list of `Where` conditions
   - `Sort`: Field name and sort direction (ASC/DESC)
   - `Page`: Limit/offset for pagination
   - `SqlQueryCriteria`: Wrapper combining where/sort/page

### PostgreSQL Implementation

Located in `sql_composer/pg/`:

- **PgSqlTranslator** (`pg_translator.py`): PostgreSQL implementation of `SqlTranslator`
  - `val_to_sql()`: Converts Python values to PostgreSQL literals with escaping
  - `where_to_sql()`: Converts `Where` conditions to SQL WHERE clauses
  - Supports parameterized queries via `*_with_params()` methods (returns tuple of SQL + parameters)
  
- **PgDataTypes** (`pg_data_types.py`): Enum of PostgreSQL data types (TEXT, INT, JSONB, UUID, etc.)

- **PgFilterOp** (`pg_filter_op.py`): Enum of PostgreSQL-specific operators including:
  - Standard comparison: EQUAL, LESS_THAN, etc.
  - Pattern matching: LIKE, ILIKE, REGEXP
  - PostgreSQL-specific: JSON operators, array operators, geometric operators, full-text search

### Extension Pattern

To support other databases (MySQL, SQLite, etc.), extend `SqlTranslator` and implement database-specific logic. For custom composer logic, extend `SqlComposer` and override methods.

### Security Notes

- Parameterized queries (`*_with_params()` methods) are preferred for user input to prevent SQL injection
- Non-parameterized methods use basic string escaping (marked "WARNING: Not sufficient for production use")
- The library supports both patterns but parameterized should be default for production

### Testing

Tests in `sql_composer_tests/` demonstrate:
- Table definition patterns (see `SandboxTable` in `sql_composer_pg_test.py`)
- Query composition with various data types
- Edge cases for string escaping, numeric values, dates, JSON
- Parameterized query generation (`parameterized_query_test.py`)
