import os
import json
import sys
import bson
import unittest
import signal

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

    return render_template('question.html', question=question, lines=[solution[i].lstrip() for i in scramble_order])



class TestCase(unittest.TestCase):
    def __init__(self, f, args, output):
        super(TestCase, self).__init__()
        self.f = f
        self.args = args
        self.output = output

    def runTest(self):
        self.assertEqual(self.f(*self.args), self.output)

@app.route('/question/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    question = get_question_from_id(question_id)
    if not question:
        return 'Question not found', 404


    given_order = json.loads(request.form.get('order', '[]'))
    given_indentation = json.loads(request.form.get('indentation', '[]'))
    correct_indentation = [int(len(line) - len(line.lstrip()))/INDENTATION_AMOUNT for line in question['solution']]


    order_correct = all([question['scramble_order'][val] == i for i, val in enumerate(given_order)])
    indentation_correct = given_indentation == correct_indentation

    if order_correct and indentation_correct:
        return 'Correct'



    lines = [question['solution'][i].strip() for i in question['scramble_order']]

    code = ''
    for i, val in enumerate(given_order):
        code += ' ' * given_indentation[i] * 4 + lines[val] + "\n"

    locals_dict = locals()
    try:
        if not code.startswith('def answer('):
            raise Exception()

        exec(code, globals(), locals_dict)
    except Exception:
        return 'Try again'

    suite = unittest.TestSuite()
    test_cases = question['test_cases']
    for test_case in test_cases:
        suite.addTest(TestCase(locals_dict['answer'], test_case['args'], test_case['output']))

    res = unittest.TextTestRunner().run(suite)

    return 'Try again' if len(res.failures) or len(res.errors) else 'Correct'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.debug = True
    app.run(host=os.getenv("IP", "0.0.0.0"), port=port)
