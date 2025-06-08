import sqlite3  # 匯入 SQLite 資料庫模組

def init_db():
    # 連接或建立名為 chat.db 的 SQLite 資料庫檔案
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()  # 建立游標，用來執行 SQL 語句

    # 建立 account 資料表（如果不存在的話）
    # 包含 id（自動遞增主鍵）、username（唯一）、email、password 四個欄位
    c.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()  # 提交變更（建立資料表）
    conn.close()   # 關閉資料庫連線


def add_account(username, email, password):
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        # 新增一筆帳號資料到 account 表
        c.execute('INSERT INTO account (username, email, password) VALUES (?, ?, ?)',
                  (username, email, password))
        conn.commit()  # 提交新增動作
        conn.close()
        return True  # 新增成功，回傳 True
    except sqlite3.IntegrityError:
        # 如果 username 重複（違反唯一性約束），會發生此錯誤，回傳 False 表示失敗
        return False


def check_account(username, password):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    # 查詢是否有符合 username 和 password 的帳號
    c.execute('SELECT * FROM account WHERE username=? AND password=?', (username, password))
    result = c.fetchone()  # 取出第一筆資料（若有）
    conn.close()
    # 若有找到符合的帳號，result 會是資料，回傳 True，否則回傳 False
    return result is not None
