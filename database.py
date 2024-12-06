import sqlite3


db = sqlite3.connect('base.db')
c = db.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS rsb(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank TEXT,
        title TEXT,
        news TEXT,
        data TEXT
    )
''')
db.commit()

def clear_database():
    #Функция для очистки базы данных.
    c.execute('DELETE FROM rsb') 
    c.execute('DELETE FROM sqlite_sequence WHERE name="rsb"')
    db.commit()
    


