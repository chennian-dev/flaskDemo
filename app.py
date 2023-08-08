from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = []
transfer_users = []

parameters = ['phone', 'mobile']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if not username or not password or not confirm_password:
            return render_template('register.html', error='Please fill in all fields')
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        hashed_password = generate_password_hash(password)
        user = {'username': username, 'password': hashed_password}
        users.append(user)
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        parameter = request.form.get('parameter')
        value = request.form.get('value')
        user = {'username': '-', 'password': '-', 'key': parameter, 'value': value}
        users.append(user)
        session['username'] = 'test'
        return redirect(url_for('dashboardtest'))
    return render_template('test.html',parameters=parameters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return render_template('login.html', error='Please fill in all fields')
        user = next((user for user in users if user['username'] == username), None)
        if not user or not check_password_hash(user['password'], password):
            return render_template('login.html', error='Invalid username or password')
        session['username'] = username
        return redirect(url_for('transfer'))
    return render_template('login.html')


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        from_account = request.form.get('from_account')
        to_account = request.form.get('to_account')
        amount = request.form.get('amount')

        # 执行转账逻辑，例如更新账户余额等操作

        transfer_user = {'from_account': from_account, 'to_account': to_account, 'amount': amount}
        transfer_users.append(transfer_user)
        session['username'] = 'test'
        return redirect(url_for('transferdemo'))

    return render_template('transfer.html')


@app.route('/transferdemo')
def transferdemo():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('transferdemo.html', username=session['username'], transfer_users=transfer_users)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], users=users)

@app.route('/dashboardtest')
def dashboardtest():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboardtest.html', username=session['username'], users=users)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)




