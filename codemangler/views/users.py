from functools import wraps

from flask import request, render_template, url_for, redirect, session

from codemangler import app, bcrypt
from codemangler.models.user import GetUser, User, CreateUser
from config import MongoConfig


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('get_login'))

    return wrap


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def get_register():
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form["username"]
    if not MongoConfig.user.find_one({'username': username}):
        return render_template('login.html', error='Username not found!')

    user = GetUser(username).get()
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        return render_template('login.html', error='Incorrect password!')

    session['username'] = user.username

    if user.user_type == 'admin':
        session['admin'] = True
        session['logged_in'] = True
        return redirect(url_for('get_admin'))
    else:
        session['logged_in'] = True
        return redirect(url_for('get_questions'))


@app.route('/signup', methods=['POST'])
def signup():
    username_check = MongoConfig.user.find({'username': request.form['username']}).count() > 0
    email_check = MongoConfig.user.find({'email': request.form['email']}).count() > 0
    if username_check and email_check:
        return render_template('signup.html', error='Username & Email already exist!')
    elif username_check:
        return render_template('signup.html', error='Username already exists!')
    elif email_check:
        return render_template('signup.html', error='Email already exists!')
    else:
        user = User(
            request.form['username'],
            request.form['repeat-password'],
            request.form['first-name'],
            request.form['last-name'],
            request.form['email'])
        CreateUser(user).populate()
        session['username'] = user.username
        session['logged_in'] = True
        return redirect(url_for('get_questions'))


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('admin', None)
    return redirect(url_for('get_login'))
