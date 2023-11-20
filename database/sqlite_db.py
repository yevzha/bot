import sqlite3 as sq

def start_database():
    global base, cur
    base = sq.connect('database/sqlite_db.db')
    cur = base.cursor()
    if base:
        print('DB connection = Done')
    base.execute("""CREATE TABLE IF NOT EXISTS article(
                   photo TEXT,
                   name TEXT,
                   text TEXT,
                   pub_date TEXT)""")
    base.commit()

def add_to_db(data):
    cur.execute("""INSERT INTO article VALUES (?,?,?,?)""", tuple(data.values()))
    base.commit()

def read_db():
    data = cur.execute("""SELECT * FROM article""").fetchall()
    return data
