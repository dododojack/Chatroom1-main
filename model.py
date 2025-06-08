import sqlite3

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_account(username, email, password):
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('INSERT INTO account (username, email, password) VALUES (?, ?, ?)',
                  (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_account(username, password):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT * FROM account WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None
