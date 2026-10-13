import sqlite3
from pathlib import Path

db_path = Path("smartevent.db").resolve()

connection = sqlite3.connect(db_path)

print("Database:", db_path)

tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name LIKE 'notifications%'
""").fetchall()

print("\nNotification tables found:")

for (table_name,) in tables:
    print(f"\nTable: {table_name}")

    columns = connection.execute(
        f'PRAGMA table_info("{table_name}")'
    ).fetchall()

    print("Columns:", [column[1] for column in columns])

    count = connection.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    ).fetchone()[0]

    print("Rows:", count)

connection.close()
