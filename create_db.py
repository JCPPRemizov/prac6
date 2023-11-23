import sqlite3

conn = sqlite3.connect('morg_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS corpses (
        id INTEGER PRIMARY KEY,
        name TEXT,
        cause_of_death TEXT,
        date_of_death DATE,
        birth_date DATE,
        age INTEGER
    )
''')
conn.commit()

conn.close()