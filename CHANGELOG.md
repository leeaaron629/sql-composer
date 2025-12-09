# Changelog

## v0.1.0 - alpha1

A type-safe SQL query builder for Python with PostgreSQL support.

### ✨ Features

#### SQL Statement Builder
- **SELECT** with column selection and table aliasing
- **INSERT** with automatic column-value mapping
- **UPDATE** with SET clause generation
- **DELETE** statement support

#### Parameterized Queries
All statement types support `*_with_params()` methods returning `(sql, params)` tuples for SQL injection protection.

#### Query Criteria
- **WHERE** - Filter conditions with 50+ PostgreSQL operators
- **ORDER BY** - Sort with `ASC`/`DESC` support
- **LIMIT/OFFSET** - Pagination support

#### PostgreSQL Operators
Comprehensive filter operators including:
- Comparison (`=`, `!=`, `<`, `<=`, `>`, `>=`)
- Pattern matching (`LIKE`, `ILIKE`, `SIMILAR TO`, regex)
- Set membership (`IN`, `NOT IN`)
- Null checks (`IS NULL`, `IS NOT NULL`)
- Range (`BETWEEN`)
- Array (`@>`, `<@`, `&&`)
- JSON (`?`, `?|`, `?&`, `@>`)
- Full-text search (`@@`)
- Network/INET operators
- Geometric operators

#### PostgreSQL Data Types
Support for: `TEXT`, `VARCHAR`, `INT`, `BIGINT`, `NUMERIC`, `BOOLEAN`, `DATE`, `TIMESTAMP`, `TIMESTAMPTZ`, `JSON`, `JSONB`, `UUID`, and more.

#### Special Handling
- **Special floats** - Proper `Infinity`, `-Infinity`, `NaN` handling
- **JSON validation** - Validates JSON strings before insertion
- **String escaping** - Automatic quote and backslash escaping

### 📦 Installation

```bash
pip install sql-composer
```

### 🚀 Quick Start

```python
from sql_composer import SqlComposer, SqlQueryCriteria, WhereClause, Where, Sort, SortType, Page
from sql_composer.pg import PgSqlTranslator, PgFilterOp

composer = SqlComposer(PgSqlTranslator(), users_table)

criteria = SqlQueryCriteria(
    where=WhereClause([Where("status", PgFilterOp.EQUAL, ["active"])]),
    sort=[Sort("name", SortType.ASC)],
    page=Page(limit=10)
)

sql, params = composer.select_with_params(columns, query_criteria=criteria)
```
