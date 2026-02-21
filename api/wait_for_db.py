import time
import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "metadata_db")
DB_USER = os.getenv("POSTGRES_USER", "metadata")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "metadata123")
DB_PORT = 5432

max_retries = 30
retry = 0

print("Waiting for database connection...")

while retry < max_retries:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        retry += 1
        print(f"Database not ready... retry {retry}/{max_retries}")
        time.sleep(2)

if retry == max_retries:
    raise Exception("Database never became ready. Exiting.")