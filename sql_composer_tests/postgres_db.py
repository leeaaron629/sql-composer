import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

def test_postgres_connection(host="localhost", database="postgres", user="postgres", password="postgres", port="5432"):
    try:
        # Connect to PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        # Execute a simple SELECT query
        cursor.execute("SELECT 1;")
        
        # Fetch the result
        result = cursor.fetchone()
        print("Connection successful! Result:", result[0])
        
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    # Example usageT
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")
    
    test_postgres_connection(host, database, user, password, port)
