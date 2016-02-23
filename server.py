#from flask import Flask, request, render_template, url_for, redirect, session
from flask import *
from pymongo import *
from functools import *
import os
import json
from bson import ObjectId

app = Flask(__name__, static_url_path='', template_folder='tmpl/')
app.secret_key = "my precious"

def get_collection(db_name, collections):
    server = 'ds059375.mongolab.com'
    port = 59375
    username = 'tanjid'
    password = 'pwd123'
    client = MongoClient(server, port)
    db = client[db_name]
    db.authenticate(username, password, mechanism='SCRAM-SHA-1')
    return db[collections]

def find_by(db_name, collections, field=""):
    posts = get_collection(db_name, collections)
    if field != "":
        question = posts.find_one({'_id': field})
        return question
    else:
        question = posts.find()
        data = []
        for item in question:
            data.append(item)
        return data


question_db = find_by("code_mangler", "questions")

def get_collection_local(db_name, collections):
    # Setting up MongoDb Connection
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    all = db[collections]
    question = all.find()
    data = []
    for item in question:
        data.append(item)
    return data

def auth_user(username, password):
    data = find_by("code_mangler", "accounts")
    for i in range(len(data)):
        print(data[i]["username"], username)
        print(data[i]["password"], password)
        if (data[i]["username"] == username and
                    data[i]["password"] == password):
            return data[i]
    return None

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #if request.form["u"] != 'dev' or request.form["p"] != 'dev123':
        user_set = auth_user(request.form["u"], request.form["p"])
        print(user_set)
        if not user_set:
            error = 'Invalid credentials. Please try again!'
        else:
            session['logged_in'] = True
            session['_id'] = str(user_set['_id'])
            return redirect(url_for('get_questions'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def get_questions():
    print("Session id:",session['_id'])
    user = find_by("code_mangler", "accounts",  ObjectId(session['_id']))
    print(user)
    data = question_db[:]
    #data = get_collection_local("question_db", "questions")
    return render_template('questions.html', questions=data, name=user["fname"]+ " " +user["lname"])

@app.route('/question/<question_id>', methods=['GET'])
@login_required
def get_question(question_id):
    temp = question_db[:]
    data = temp[int(question_id)-1]
    #data = get_collection_local("question_db", "questions")
    solution = data['solution']
    scramble_order = data['scramble_order']
    return render_template(
        'question.html',
        id=data['id'],
        question=data['question'],
        description=data['description'],
        #lines=[solution[i].lstrip() for i in scramble_order]
        lines = [solution[i] for i in scramble_order]
    )

@app.route('/question/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    ans = json.loads(request.form.get('answer', '[]'))
    data = question_db[int(question_id)-1]
    return 'Correct' if ans == data['scramble_order'] else 'Try Again'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    # Setting up local server for Flask
    app.debug = True
    app.run(port=port)
