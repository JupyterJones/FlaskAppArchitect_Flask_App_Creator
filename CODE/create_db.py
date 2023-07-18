import sqlite3

# Create a connection to the database
conn = sqlite3.connect('code.db')
cursor = conn.cursor()

# Create the code table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS code (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        code TEXT,
        keywords text
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
