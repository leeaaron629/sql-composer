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
        
        create_data_table_sql = """
            CREATE TABLE IF NOT EXISTS all_data_types (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                bigint_col BIGINT,
                bigserial_col BIGSERIAL,
                bit_col BIT(8),
                varbit_col BIT VARYING(64),
                boolean_col BOOLEAN,
                box_col BOX,
                bytea_col BYTEA,
                char_col CHARACTER(10),
                varchar_col CHARACTER VARYING(255),
                cidr_col CIDR,
                circle_col CIRCLE,
                date_col DATE,
                double_col DOUBLE PRECISION,
                inet_col INET,
                integer_col INTEGER,
                interval_col INTERVAL,
                json_col JSON,
                jsonb_col JSONB,
                line_col LINE,
                lseg_col LSEG,
                macaddr_col MACADDR,
                macaddr8_col MACADDR8,
                money_col MONEY,
                numeric_col NUMERIC(10,2),
                decimal_col DECIMAL(10,2),
                path_col PATH,
                pg_lsn_col PG_LSN,
                pg_snapshot_col PG_SNAPSHOT,
                point_col POINT,
                polygon_col POLYGON,
                real_col REAL,
                smallint_col SMALLINT,
                smallserial_col SMALLSERIAL,
                serial_col SERIAL,
                text_col TEXT,
                time_col TIME,
                time_tz_col TIME WITH TIME ZONE,
                timestamp_col TIMESTAMP,
                timestamptz_col TIMESTAMP WITH TIME ZONE,
                tsquery_col TSQUERY,
                tsvector_col TSVECTOR,
                xml_col XML
            );
        """

        create_random_row_sql = """
            INSERT INTO all_data_types (
                bigint_col,
                bigserial_col,
                bit_col,
                varbit_col,
                boolean_col,
                box_col,
                bytea_col,
                char_col,
                varchar_col,
                cidr_col,
                circle_col,
                date_col,
                double_col,
                inet_col,
                integer_col,
                interval_col,
                json_col,
                jsonb_col,
                line_col,
                lseg_col,
                macaddr_col,
                macaddr8_col,
                money_col,
                numeric_col,
                decimal_col,
                path_col,
                pg_lsn_col,
                pg_snapshot_col,
                point_col,
                polygon_col,
                real_col,
                smallint_col,
                smallserial_col,
                serial_col,
                text_col,
                time_col,
                time_tz_col,
                timestamp_col,
                timestamptz_col,
                tsquery_col,
                tsvector_col,
                xml_col
            ) VALUES (
                9223372036854775807,  -- bigint_col (max value)
                DEFAULT,  -- bigserial_col (auto-incrementing)
                B'10101010',  -- bit_col
                B'1111000011110000',  -- varbit_col
                true,  -- boolean_col
                '((1,1),(2,2))',  -- box_col
                '\\xDEADBEEF',  -- bytea_col
                'CHAR10PAD',  -- char_col
                'Variable length text',  -- varchar_col
                '192.168.100.128/25',  -- cidr_col
                '<(1,1),2>',  -- circle_col
                '2024-03-14',  -- date_col
                3.14159265359,  -- double_col
                '192.168.1.1',  -- inet_col
                42,  -- integer_col
                '1 year 2 months 3 days 4 hours 5 minutes 6 seconds',  -- interval_col
                '{"key": "value", "number": 42}',  -- json_col
                '{"nested": {"array": [1, 2, 3]}}',  -- jsonb_col
                '{1,-2,3}',  -- line_col
                '[(1,1),(2,2)]',  -- lseg_col
                '08:00:2b:01:02:03',  -- macaddr_col
                '08:00:2b:01:02:03:04:05',  -- macaddr8_col
                '$1234.56',  -- money_col
                123456.78,  -- numeric_col
                987654.32,  -- decimal_col
                '((1,1),(2,2),(3,3))',  -- path_col
                '0/0',  -- pg_lsn_col
                '10:20:10,14,15',  -- pg_snapshot_col
                '(1,1)',  -- point_col
                '((1,1),(2,2),(3,3),(1,1))',  -- polygon_col
                3.14,  -- real_col
                32767,  -- smallint_col
                DEFAULT,  -- smallserial_col (auto-incrementing)
                DEFAULT,  -- serial_col (auto-incrementing)
                'This is a long text field that can store unlimited characters',  -- text_col
                '15:30:00',  -- time_col
                '15:30:00-07',  -- time_tz_col
                '2024-03-14 15:30:00',  -- timestamp_col
                '2024-03-14 15:30:00-07',  -- timestamptz_col
                'web & development',  -- tsquery_col
                'The quick brown fox jumps over the lazy dog',  -- tsvector_col
                '<?xml version="1.0"?><root><element>value</element></root>'  -- xml_col
            );
        """

        cursor.execute(create_data_table_sql)
        cursor.execute(create_random_row_sql)
        connection.commit()  # Commit the table creation and insert
        print("Table 'all_data_types' created successfully and sample row inserted!")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", str(error))
        
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    # Example usage
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")
    
    test_postgres_connection(host, database, user, password, port)
