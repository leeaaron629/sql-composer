# sql-composer

A type-safe SQL query builder and composer for Python with PostgreSQL support.

[![PyPI version](https://img.shields.io/pypi/v/shiba-sql-composer.svg)](https://pypi.org/project/shiba-sql-composer/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- **Type-safe query building** — Define your tables with typed columns for safer SQL generation
- **PostgreSQL support** — Full support for PostgreSQL data types and operators
- **Parameterized queries** — Built-in support for parameterized queries to prevent SQL injection
- **Rich filtering** — 40+ filter operators including comparison, pattern matching, JSON, arrays, and more
- **Query composition** — Easily compose SELECT, INSERT, UPDATE, and DELETE queries
- **Pagination & sorting** — Built-in support for ORDER BY, LIMIT, and OFFSET

## Installation

```bash
pip install shiba-sql-composer
```

## Quick Start

### 1. Define Your Table

```python
from sql_composer import Table, Column
from sql_composer.pg.pg_data_types import PgDataTypes

class UsersTable(Table):
    id = Column("id", PgDataTypes.INT)
    name = Column("name", PgDataTypes.TEXT)
    email = Column("email", PgDataTypes.VARCHAR)
    age = Column("age", PgDataTypes.INT)
    created_at = Column("created_at", PgDataTypes.TIMESTAMP)
```

### 2. Create a Composer

```python
from sql_composer import SqlComposer
from sql_composer.pg.pg_translator import PgSqlTranslator

# Initialize table and composer
users = UsersTable("users")
composer = SqlComposer(PgSqlTranslator(), users)
```

### 3. Build Queries

**SELECT query:**

```python
# Simple select
sql = composer.select(columns=[users.id, users.name, users.email])
# SELECT id, name, email FROM users
```

**SELECT with filtering, sorting, and pagination:**

```python
from sql_composer import Where, WhereClause, Sort, SortType, Page, SqlQueryCriteria
from sql_composer.pg.pg_filter_op import PgFilterOp

query_criteria = SqlQueryCriteria(
    where=WhereClause([
        Where("age", PgFilterOp.GREATER_THAN, [18]),
        Where("name", PgFilterOp.LIKE, ["%John%"]),
    ]),
    sort=[Sort("created_at", SortType.DESC)],
    page=Page(limit=10, offset=0),
)

sql = composer.select(
    columns=users.columns,
    query_criteria=query_criteria
)
# SELECT id, name, email, age, created_at
# FROM users
# WHERE age > 18
# AND name LIKE '%John%'
# ORDER BY created_at DESC
# LIMIT 10 OFFSET 0
```

**INSERT query:**

```python
sql = composer.insert({
    "name": "Jane Doe",
    "email": "jane@example.com",
    "age": 28,
})
# INSERT INTO users (name, email, age) VALUES ('Jane Doe', 'jane@example.com', 28);
```

**UPDATE query:**

```python
sql = composer.update({
    "name": "Jane Smith",
    "age": 29,
})
# UPDATE users SET name = 'Jane Smith', age = 29;
```

### 4. Parameterized Queries (Recommended)

For production use, use parameterized queries to prevent SQL injection:

```python
# Parameterized SELECT
sql, params = composer.select_with_params(
    columns=users.columns,
    query_criteria=query_criteria
)
# sql: "SELECT ... WHERE age > %s AND name LIKE %s ..."
# params: [18, "%John%"]

# Parameterized INSERT
sql, params = composer.insert_with_params({
    "name": "Jane Doe",
    "email": "jane@example.com",
})
# sql: "INSERT INTO users (name, email) VALUES (%s, %s);"
# params: ["Jane Doe", "jane@example.com"]

# Execute with psycopg2
cursor.execute(sql, params)
```

## Supported Filter Operators

| Category | Operators |
|----------|-----------|
| **Comparison** | `EQUAL`, `NOT_EQUAL`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL` |
| **Pattern Matching** | `LIKE`, `NOT_LIKE`, `ILIKE`, `NOT_ILIKE`, `SIMILAR_TO`, `REGEXP`, `REGEXP_CASE_INSENSITIVE` |
| **Set Membership** | `IN`, `NOT_IN` |
| **Null Checks** | `IS_NULL`, `IS_NOT_NULL` |
| **Range** | `BETWEEN`, `NOT_BETWEEN` |
| **Array** | `CONTAINS`, `IS_CONTAINED_BY`, `OVERLAPS` |
| **JSON** | `JSON_CONTAINS`, `JSON_HAS_KEY`, `JSON_HAS_ANY_KEY`, `JSON_HAS_ALL_KEYS` |
| **Full Text** | `FULLTEXT_MATCH`, `FULLTEXT_QUERY` |

## Supported PostgreSQL Data Types

- **String:** `TEXT`, `VARCHAR`, `CHAR`
- **Integer:** `INT`, `BIGINT`, `SMALLINT`
- **Numeric:** `NUMERIC`, `DECIMAL`, `REAL`, `DOUBLE_PRECISION`
- **Boolean:** `BOOLEAN`
- **Date/Time:** `DATE`, `TIMESTAMP`, `TIMESTAMPTZ`, `TIME`
- **JSON:** `JSON`, `JSONB`
- **Other:** `UUID`

## Supported Databases

- ✅ PostgreSQL

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Clone the repository
git clone https://github.com/leeaaron629/sql-composer.git
cd sql-composer

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
