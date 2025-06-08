from flask import Flask, request, render_template, redirect, url_for, make_response, session, flash
from model import init_db, add_account, check_account  # 確定有這個model.py和這些函式

app = Flask(__name__)
app.secret_key = "your_secret_key"  # session 必須

# 初始化資料庫
init_db()

# 訊息暫存（單機測試用，全域變數不適合多人）
messages = []

@app.route('/')
def index():
        # 如果 session 裡有 username，代表已登入，直接導向聊天室頁面

    if 'username' in session:
        return redirect(url_for('chatroom'))
    else:
                # 沒登入就導向登入頁面

        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 取得表單資料，並去除頭尾空白
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # 檢查是否有欄位沒填
        if not username or not email or not password:
            flash("請填寫所有欄位！")  # flash 訊息會在模板裡顯示
            return redirect(url_for('register'))  # 重新導向註冊頁

        # 嘗試新增帳號，成功回傳 True，失敗（帳號重複）回傳 False
        success = add_account(username, email, password)
        if success:
            flash("註冊成功！請登入。")
            return redirect(url_for('login'))  # 註冊成功導向登入頁
        else:
            flash("帳號已存在，請換一個使用者名稱。")
            return redirect(url_for('register'))  # 帳號重複，重新註冊頁

    # GET 請求呈現註冊頁面
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 取得表單資料
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # 檢查帳號密碼是否正確
        if check_account(username, password):
            session['username'] = username  # 登入成功，將 username 存進 session
            flash(f"歡迎登入，{username}！")
            return redirect(url_for('chatroom'))  # 導向聊天室
        else:
            flash("帳號或密碼錯誤！")
            return redirect(url_for('login'))  # 登入失敗重新登入

    # GET 請求呈現登入頁面
    return render_template('login.html')


@app.route('/logout')
def logout():
    # 清除 session 中的 username 代表登出
    session.pop('username', None)
    flash("你已登出。")
    return redirect(url_for('login'))  # 登出後回登入頁


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    # 未登入的使用者，直接跳轉登入頁
    if 'username' not in session:
        flash("請先登入！")
        return redirect(url_for('login'))

    # POST 代表使用者送出新訊息
    if request.method == 'POST':
        msg = request.form.get('message').strip()
        if msg:
            # 將訊息加上使用者名稱，放入全域訊息暫存列表
            messages.append(f"{session['username']}: {msg}")

    # 顯示聊天室頁面，並帶入目前所有訊息與使用者名稱
    return render_template('chatroom.html', messages=messages, username=session['username'])


if __name__ == '__main__':
    # 啟動 Flask 伺服器，debug 模式開啟方便除錯
    app.run(host='127.0.0.1', port=5000, debug=True)
