import sqlite3


connect = sqlite3.connect('db.sqlite3')
cur = connect.cursor()

cur.execute(
    'DROP TABLE telegram;'
)

connect.commit()
connect.close()
