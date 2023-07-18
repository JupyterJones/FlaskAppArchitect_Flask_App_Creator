import sqlite3

db = sqlite3.connect('code.db')
cursor = db.cursor()

rows = cursor.execute("Select ROWID, * from snippets")
for row in rows:
    print(row[0])
    print(row[1])
    print(row[2])
    print(row[3])
    print("---------------")
db.close()

