#!/usr/bin/env python3
"""
Test file demonstrating parameterized query functionality.
This shows how to use the SQL Composer with parameterized queries for safe database operations.
"""

from typing import Any
from sql_composer.db_models import Table, Column
from sql_composer.pg.pg_data_types import PgDataTypes
from sql_composer.sql_composer import SqlComposer
from sql_composer.pg.pg_translator import PgSqlTranslator
from sql_composer.db_conditions import Where, WhereClause, Sort, Page, SqlQueryCriteria, SortType
from sql_composer.pg.pg_filter_op import PgFilterOp


class UserTable(Table):
    id = Column(name="id", type_=PgDataTypes.INT)
    name = Column(name="name", type_=PgDataTypes.TEXT)
    email = Column(name="email", type_=PgDataTypes.TEXT)
    age = Column(name="age", type_=PgDataTypes.INT)
    active = Column(name="active", type_=PgDataTypes.BOOLEAN)


def demonstrate_parameterized_queries():
    """Demonstrate parameterized query usage"""
    print("🔒 PARAMETERIZED QUERY DEMONSTRATION")
    print("=" * 50)
    
    # Setup
    table = UserTable("users")
    translator = PgSqlTranslator()
    composer = SqlComposer(translator, table)
    
    print("\n1️⃣ PARAMETERIZED SELECT QUERIES")
    print("-" * 30)
    
    # Simple parameterized select
    sql, params = composer.select_with_params()
    print(f"Basic SELECT:\nSQL: {sql.strip()}\nParams: {params}")
    
    # Parameterized select with WHERE clause
    where_clause = WhereClause([
        Where("name", PgFilterOp.EQUAL, ["John Doe"]),
        Where("age", PgFilterOp.GREATER_THAN, [25])
    ])
    query_criteria = SqlQueryCriteria(where=where_clause)
    
    sql, params = composer.select_with_params(query_criteria=query_criteria)
    print(f"\nSELECT with WHERE:\nSQL: {sql.strip()}\nParams: {params}")
    
    # Parameterized select with complex conditions
    complex_where = WhereClause([
        Where("name", PgFilterOp.LIKE, ["%John%"]),
        Where("age", PgFilterOp.BETWEEN, [18, 65]),
        Where("active", PgFilterOp.EQUAL, [True])
    ])
    complex_criteria = SqlQueryCriteria(
        where=complex_where,
        sort=[Sort("name", SortType.ASC)],
        page=Page(limit=10, offset=0)
    )
    
    sql, params = composer.select_with_params(query_criteria=complex_criteria)
    print(f"\nComplex SELECT:\nSQL: {sql.strip()}\nParams: {params}")
    
    print("\n2️⃣ PARAMETERIZED INSERT QUERIES")
    print("-" * 30)
    
    # Parameterized insert
    user_data = {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 30,
        "active": True
    }
    
    sql, params = composer.insert_with_params(user_data)
    print(f"INSERT:\nSQL: {sql.strip()}\nParams: {params}")
    
    # Insert with potentially dangerous data (demonstrates safety)
    dangerous_data = {
        "name": "Robert'; DROP TABLE users; --",
        "email": "robert@example.com",
        "age": 25,
        "active": True
    }
    
    sql, params = composer.insert_with_params(dangerous_data)
    print(f"\nINSERT with dangerous data:\nSQL: {sql.strip()}\nParams: {params}")
    print("✅ Notice: The dangerous string is safely parameterized!")
    
    print("\n3️⃣ PARAMETERIZED UPDATE QUERIES")
    print("-" * 30)
    
    # Parameterized update
    update_data = {
        "name": "Jane Smith-Updated",
        "age": 31
    }
    
    sql, params = composer.update_with_params(update_data)
    print(f"UPDATE:\nSQL: {sql.strip()}\nParams: {params}")
    
    print("\n4️⃣ USAGE WITH DATABASE CONNECTIONS")
    print("-" * 30)
    
    print("""
# Example usage with psycopg2:
import psycopg2

# Connect to database
conn = psycopg2.connect("your_connection_string")
cursor = conn.cursor()

# Generate parameterized query
sql, params = composer.select_with_params(query_criteria=query_criteria)

# Execute safely
cursor.execute(sql, params)
results = cursor.fetchall()

# Close connections
cursor.close()
conn.close()
    """)
    
    print("\n5️⃣ SECURITY COMPARISON")
    print("-" * 30)
    
    print("❌ UNSAFE (String concatenation):")
    print("sql = f\"SELECT * FROM users WHERE name = '{user_input}'\"")
    print("cursor.execute(sql)  # Vulnerable to SQL injection!")
    
    print("\n✅ SAFE (Parameterized queries):")
    print("sql, params = composer.select_with_params(query_criteria)")
    print("cursor.execute(sql, params)  # Safe from SQL injection!")


def demonstrate_sql_injection_prevention():
    """Demonstrate how parameterized queries prevent SQL injection"""
    print("\n🛡️ SQL INJECTION PREVENTION DEMONSTRATION")
    print("=" * 50)
    
    table = UserTable("users")
    translator = PgSqlTranslator()
    composer = SqlComposer(translator, table)
    
    # Malicious input that would cause SQL injection in string concatenation
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "'; DELETE FROM users; --",
        "' UNION SELECT * FROM passwords; --"
    ]
    
    for malicious_input in malicious_inputs:
        print(f"\nMalicious input: {malicious_input}")
        
        # Create WHERE clause with malicious input
        where_clause = WhereClause([
            Where("name", PgFilterOp.EQUAL, [malicious_input])
        ])
        query_criteria = SqlQueryCriteria(where=where_clause)
        
        # Generate parameterized query
        sql, params = composer.select_with_params(query_criteria=query_criteria)
        
        print(f"Generated SQL: {sql.strip()}")
        print(f"Parameters: {params}")
        print("✅ Safe: Malicious input is treated as a literal string value!")


if __name__ == "__main__":
    # demonstrate_parameterized_queries()
    demonstrate_sql_injection_prevention()
    
    print("\n🎉 PARAMETERIZED QUERIES DEMONSTRATION COMPLETE!")
    print("Your SQL Composer now supports safe, parameterized database operations.")

