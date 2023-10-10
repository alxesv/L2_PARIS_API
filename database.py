import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")

conn = psycopg2.connect(f"dbname={db_name} user={db_user}")
cur = conn.cursor()

cur.execute("SELECT * FROM test_table;")

records = cur.fetchall()

print(records)