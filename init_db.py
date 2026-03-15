import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE expenses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
amount REAL,
category TEXT
)
""")

conn.close()

print("Database created")