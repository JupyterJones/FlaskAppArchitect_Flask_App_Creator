import sqlite3

db = sqlite3.connect('code.db')
cursor = db.cursor()

cursor.execute("CREATE TABLE if not exists snippets (id INTEGER PRIMARY KEY, description TEXT, code TEXT, keywords TEXT)")

db.commit()
