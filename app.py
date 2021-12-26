from datetime import timedelta
from flask import Flask,render_template,request,session,g
from flask.helpers import url_for
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from loginform import LoginForm
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        g.user = session['username']

def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM adminuser WHERE username = %s AND password = %s', (username,password))
        
        account = cursor.fetchone()
        print(account)
        mysql.connect.commit()
        cursor.close()
        if account:
            session['loggedin'] = True
            session['username'] = account[1]
            msg = 'Correct'
            if account[5] == 'admin':
                return redirect(url_for('dashboard'))
            # elif account[5] == 'employee':
            #     return redirect(url_for('index'))

            # return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect'
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('login.html', form = form , msg = msg)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)