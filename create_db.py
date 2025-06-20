import sqlite3

def create_database():
    conn = sqlite3.connect('app_db.db')

    with open('create_table.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
        conn.executescript(sql_script)

    conn.commit()
    conn.close()

create_database()