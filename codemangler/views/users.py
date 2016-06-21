import httplib2
import json
import os
import sys

from functools import wraps
from codemangler import app
from codemangler.models.user import User, UserModel
from config import MongoConfig
from flask import request, render_template, url_for, redirect, session
from oauth2client.client import OAuth2WebServerFlow

# TODO: move values to config
FLOW = OAuth2WebServerFlow(client_id=os.environ['UTEACH_OAUTH2_CLIENT_ID'],
                           client_secret=os.environ['UTEACH_OAUTH2_CLIENT_SECRET'],
                           auth_uri='https://umairidris.auth0.com/authorize',
                           token_uri='https://umairidris.auth0.com/oauth/token',
                           scope='openid name email nickname',
                           redirect_uri='http://localhost:8000/oauth2callback')
AUTH_URL = FLOW.step1_get_authorize_url() + '&connection=Username-Password-Authentication'
REQUIRED_RESPONSE_KEYS = ['email', 'name', 'nickname']


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
            return redirect(AUTH_URL)

    return wrap

@app.route('/login')
def get_login():
    return redirect(AUTH_URL)

@app.route('/oauth2callback')
def oauth2_callback():
    error = request.args.get('error')
    if error:
        return '{error}: {error_description}'.format(error=error, error_description=request.args.get('error_description')), 401

    code = request.args.get('code')
    if not code:
        return 'No code given', 401

    credentials = FLOW.step2_exchange(code)
    http = httplib2.Http()
    http = credentials.authorize(http)
    response, content = http.request('https://umairidris.auth0.com/userinfo')

    if response.status != 200:
        return response.reason, response.status

    user_dict = json.loads(content.decode("utf-8"))

    for key in REQUIRED_RESPONSE_KEYS:
        if key not in user_dict:
            return 'Missing {key} in response'.format(key=key), 401

    user = UserModel.get({'email': user_dict['email']})

    if not user: # new user
        # username is email for now
        user = User(user_dict['email'], user_dict['nickname'], user_dict['email'])
        user = UserModel.create(user)

        if not user:
            return 'Failed to create user', 500

    session['username'] = user.username
    session['logged_in'] = True

    if user.user_type == 'admin':
        session['admin'] = True
        return redirect(url_for('get_admin'))

    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    """ () -> rendered_template

    Returns the rendered template of login.html,
    after the user makes a POST request to 'logout'
    """
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('admin', None)
    return redirect('/')
