import sqlite3

# Create a connection to the database
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
