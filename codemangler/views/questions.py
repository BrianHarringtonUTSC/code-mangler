import json
import os
import subprocess
import tempfile
from random import shuffle

from bson import ObjectId
from flask import request, render_template, session, redirect, url_for

from codemangler import app, db
from codemangler.models.question import GetQuestion, Question, CreateQuestion
from codemangler.models.user import GetUser, UpdateUser, User, CreateUser
from codemangler.views.users import login_required
from config import MongoConfig

INDENTATION_AMOUNT = 4
RESPONSE_SUCCESS = 'Correct'
RESPONSE_FAILED = 'Try Again'


@app.route('/')
@login_required
def get_questions():
    if 'logged_in' in session and 'username' in session:
        user = GetUser(session['username']).get()
    questions = db.questions.find()

    return render_template('questions.html', questions=questions, completed=user.completed,
                       name=user.first_name + " " + user.last_name)




@app.route('/question/<question_id>', methods=['GET'])
@login_required
def get_question(question_id):
    question = GetQuestion(ObjectId(question_id)).get()
    if not question:
        return 'Question not found', 404

    solution = question.solution
    scramble_order = question.scramble_order

    return render_template('question.html', question=question,
                           lines=[solution[i].lstrip() for i in scramble_order])


def run_test_cases(question, given_order, given_indentation):
    lines = [question.solution[i].strip() for i in question.scramble_order]

    code = ''
    for i, val in enumerate(given_order):
        code += ' ' * given_indentation[i] * INDENTATION_AMOUNT + lines[val] + "\n"

    for test_case in question.test_cases:
        code += "\n" + test_case

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bytes(code, 'UTF-8'))

    try:
        # TODO: pass in python location as an arg so you can specify
        with open(os.devnull, 'w') as devnull:  # redirect output to dev null
            res = subprocess.run(["python", f.name], stdout=devnull, stderr=devnull, timeout=1)
            res.check_returncode()
    except Exception:
        return False
    finally:
        os.remove(f.name)

    return True


def check_answer(question, given_order, given_indentation):
    correct_indentation = [int(len(line) - len(line.lstrip())) / INDENTATION_AMOUNT for line in question.solution
                           ]

    order_correct = all([question.scramble_order[val] == i for i, val in enumerate(given_order)])
    indentation_correct = given_indentation == correct_indentation

    if order_correct and indentation_correct:
        return True

    if not question.test_cases:
        return False

    return run_test_cases(question, given_order, given_indentation)


@app.route('/question/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    question = GetQuestion(ObjectId(question_id)).get()
    if not question:
        return 'Question not found', 404

    given_order = json.loads(request.form.get('order', '[]'))
    given_indentation = json.loads(request.form.get('indentation', '[]'))
    user = GetUser(session["username"]).get()
    if ObjectId(question_id) not in user.attempted and user.completed:
        user.attempted.append(ObjectId(question_id))
    UpdateUser(user).post()
    user = GetUser(session["username"]).get()
    print(user.username, user.first_name, user.attempted, user.completed)

    if check_answer(question, given_order, given_indentation):
        if ObjectId(question_id) not in user.completed:
            user.completed.append(ObjectId(question_id))
        user.attempted.remove(ObjectId(question_id))
        UpdateUser(user).post()
        return RESPONSE_SUCCESS
    else:
        return RESPONSE_FAILED