import os
import psycopg2

def init_database():
    """Initialize the database using the schema file."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "mydb"),
        )
        with conn.cursor() as cur:
            # Read schema file
            schema_file = os.path.join(os.path.dirname(__file__), 'db/my_table_ddl.sql')
            with open(schema_file, 'r') as file:
                ddl = file.read()
                cur.execute(ddl)
                conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()