from functools import wraps

from flask import request, render_template, url_for, redirect, session

from codemangler import app, bcrypt
from codemangler.models.user import GetUser, User, CreateUser
from config import MongoConfig


def login_required(f):
    """ (function) -> function

    Wrap views for users so that only
    logged in users can view those pages
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('get_login'))

    return wrap


@app.route('/adminlogin', methods=['GET'])
def get_login():
    """ () -> rendered_template

    Returns the rendered template of login.html
    after the user makes a GET request to 'login'
    """
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def get_register():
    """ () -> rendered_template

    Returns the rendered template of signup.html
    after the user makes a GET request to 'signup'
    """
    return render_template('signup.html')


@app.route('/adminlogin', methods=['POST'])
def login_user():
    """ () -> rendered_template

    Returns the rendered template of admin.html or questions.html according
    to data from user input , after the user makes a POST request to 'login'
    """
    username = request.form["username"]
    if not MongoConfig.user.find_one({'username': username}):
        return render_template('login.html', error='Username not found!')

    user = GetUser(username).get()
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        return render_template('login.html', error='Incorrect password!')

    session['username'] = user.username

    # If user type is admin then redirect to admin side #
    # If user type is regular then redirect to user side #
    if user.user_type == 'admin':
        session['admin'] = True
        session['logged_in'] = True
        return redirect(url_for('get_admin'))
    else:
        session['logged_in'] = True
        return redirect(url_for('get_questions'))


@app.route('/signup', methods=['POST'])
def signup():
    """ () -> rendered_template

    Returns the rendered template of questions.html
    according to data from user input for registration,
    after the user makes a POST request to 'login'
    """
    username_check = MongoConfig.user.find({'username': request.form['username']}).count() > 0
    email_check = MongoConfig.user.find({'email': request.form['email']}).count() > 0

    # Check if username or email already exists #
    if username_check and email_check:
        return render_template('signup.html', error='Username & Email already exist!')
    elif username_check:
        return render_template('signup.html', error='Username already exists!')
    elif email_check:
        return render_template('signup.html', error='Email already exists!')
    else:
        # If username and email doesn't exist #
        # then create a new user instance #
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
    """ () -> rendered_template

    Returns the rendered template of login.html,
    after the user makes a POST request to 'logout'
    """
    # Drop data from the cache #
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('admin', None)
    return redirect(url_for('get_login'))
