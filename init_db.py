import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), 'inventory.db')

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the 'items' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database 'inventory.db' and table 'items' created successfully at {db_path}")
