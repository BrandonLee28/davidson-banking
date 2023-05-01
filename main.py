from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from user import User

app = Flask(__name__)
app.secret_key = 'dogseatpoop'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Load user from database
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('.\sql_db\Demo_table.db')
    cur = conn.cursor()
    query = "SELECT * FROM user WHERE user_id = ?"
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        return None
    return User(user[0], user[1], user[2], user[3], user[4])


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')
# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = sqlite3.connect('.\sql_db\Demo_table.db')
        cur = conn.cursor()
        name = request.form['name']
        email = request.form['username']
        password = request.form['password']
        query = "Insert Into user ('email','password','money','name') Values(?,?,?,?)"
        cur.execute(query,(email,password,0,name))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('signup.html')



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect('.\sql_db\Demo_table.db')
        cur = conn.cursor()
        email = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM user WHERE email = ?"
        cur.execute(query, (email,))
        user = cur.fetchone()
        conn.close()
        if user is not None and user[2] == password:
            user_obj = User(user[0], user[1], user[2], user[3],user[4])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        if "depositamount" in request.form:
            conn = sqlite3.connect('.\sql_db\Demo_table.db')
            cur = conn.cursor()
            amount = request.form['depositamount']
            userid = current_user.get_id()
            query = "UPDATE user SET money = money + ? WHERE user_id = ?"
            cur.execute(query,(amount,userid))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
            
        if "withdrawamount" in request.form:
            conn = sqlite3.connect('.\sql_db\Demo_table.db')
            cur = conn.cursor()
            amount = request.form['withdrawamount']
            userid = current_user.get_id()
            query = "UPDATE user SET money = money - ? WHERE user_id = ?"
            cur.execute(query,(amount,userid))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user = current_user)

if __name__ == '__main__':
    app.run(debug=True)
