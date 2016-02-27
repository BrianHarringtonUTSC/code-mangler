import os
import json
import sys
import bson

from flask import Flask, request, render_template, url_for, redirect, session
from pymongo import MongoClient
from functools import wraps
from bson import ObjectId

app = Flask(__name__, static_url_path='')
app.secret_key = "my precious"

DB_URI = 'mongodb://tanjid:pwd123@ds059375.mongolab.com:59375/code_mangler'
client = MongoClient(DB_URI)
db = client.code_mangler

INDENTATION_AMOUNT = 4

path = '/home/leoumair/'
if path not in sys.path:
   sys.path.append(path)


def get_session_user():
    if 'logged_in' in session and 'user_id' in session:
        return db.accounts.find_one({"_id": ObjectId(session['user_id'])})

def get_question_from_id(question_id):
    try:
        qid = ObjectId(question_id)
    except bson.errors.InvalidId as e:
        return None

    return db.questions.find_one({"_id": qid})

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

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form["u"]
    password = request.form["p"]
    user = db.accounts.find_one({'username': username, 'password': password})

    if user:
        session['user_id'] = str(user['_id'])
        session['logged_in'] = True
        return redirect(url_for('get_questions'))

    return render_template('login.html', error='Invalid credentials. Please try again!')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('get_login'))

@app.route('/')
@login_required
def get_questions():
    user = get_session_user()
    questions = db.questions.find()
    return render_template('questions.html', questions=questions, name=user["fname"] + " " + user["lname"])

@app.route('/question/<question_id>', methods=['GET'])
@login_required
def get_question(question_id):
    question = get_question_from_id(question_id)
    if not question:
        return 'Question not found', 404

    solution = question['solution']
    scramble_order = question['scramble_order']
    return render_template(
        'question.html',
        question=question,
        lines=[solution[i].lstrip() for i in scramble_order]
    )

@app.route('/question/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    question = get_question_from_id(question_id)
    if not question:
        return 'Question not found', 404


    given_order = json.loads(request.form.get('order', '[]'))
    given_indentation = json.loads(request.form.get('indentation', '[]'))
    correct_indentation = [int(len(line) - len(line.lstrip()))/INDENTATION_AMOUNT for line in question['solution']]

    print(given_order, question['scramble_order'], file=sys.stderr)
    print(given_indentation, correct_indentation, file=sys.stderr)

    if given_order == question['scramble_order'] and given_indentation == correct_indentation:
        return 'Correct'
    else:
        return 'Try Again'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.debug = True
    #app.run(port=port)
    app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8080)))
