import sqlite3
from config import DATA_DIR, DB_PATH

SQL_FILE = DATA_DIR / "schema.sql"

def create_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Legge lo schema dal file
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Esegue tutto lo script
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"Database '{DB_PATH}' creato con successo!")

if __name__ == "__main__":
    create_db()
