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
    if 'username' in session:
        return redirect(url_for('chatroom'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        if not username or not email or not password:
            flash("請填寫所有欄位！")
            return redirect(url_for('register'))

        success = add_account(username, email, password)
        if success:
            flash("註冊成功！請登入。")
            return redirect(url_for('login'))
        else:
            flash("帳號已存在，請換一個使用者名稱。")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if check_account(username, password):
            session['username'] = username
            flash(f"歡迎登入，{username}！")
            return redirect(url_for('chatroom'))
        else:
            flash("帳號或密碼錯誤！")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("你已登出。")
    return redirect(url_for('login'))

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if 'username' not in session:
        flash("請先登入！")
        return redirect(url_for('login'))

    if request.method == 'POST':
        msg = request.form.get('message').strip()
        if msg:
            messages.append(f"{session['username']}: {msg}")

    return render_template('chatroom.html', messages=messages, username=session['username'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
