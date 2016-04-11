import json
import os
import subprocess
import tempfile

from bson import ObjectId, errors
from flask import request, render_template, url_for, session

from codemangler import app, db, bcrypt
from codemangler.views.users import login_required
from codemangler.models.user import Get, User, Create
from config import MongoConfig

INDENTATION_AMOUNT = 4
RESPONSE_SUCCESS = 'Correct'
RESPONSE_FAILED = 'Try Again'


@app.route('/')
@login_required
def get_questions():
    if 'logged_in' in session and 'username' in session:
        user = Get(session['username']).get()
    questions = db.questions.find()
    return render_template('questions.html', questions=questions,
                           name=user.first_name + " " + user.last_name)


@app.route('/upload')
@login_required
def upload_page():
    if 'logged_in' in session and 'username' in session:
        user = Get(session['username']).get()
    return render_template('upload.html', name=user.first_name + " " + user.last_name)


@app.route('/question/<question_id>', methods=['GET'])
@login_required
def get_question(question_id):
    question = get_question_from_id(question_id)
    if not question:
        return 'Question not found', 404

    solution = question['solution']
    scramble_order = question['scramble_order']

    return render_template('question.html', question=question,
                           lines=[solution[i].lstrip() for i in scramble_order])


def get_question_from_id(question_id):
    try:
        qid = ObjectId(question_id)
    except errors.InvalidId as e:
        return None

    return db.questions.find_one({"_id": qid})


def run_test_cases(question, given_order, given_indentation):
    lines = [question['solution'][i].strip() for i in question['scramble_order']]

    code = ''
    for i, val in enumerate(given_order):
        code += ' ' * given_indentation[i] * INDENTATION_AMOUNT + lines[val] + "\n"

    for test_case in question['test_cases']:
        code += "\n" + test_case

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(bytes(code, 'UTF-8'))

    try:
        # TODO: pass in python location as an arg so you can specify
        with open(os.devnull, 'w') as devnull: # redirect output to dev null
            res = subprocess.run(["python", f.name], stdout=devnull, stderr=devnull, timeout=1)
            res.check_returncode()
    except Exception:
        return False
    finally:
        os.remove(f.name)

    return True

def check_answer(question, given_order, given_indentation):

    correct_indentation = [int(len(line) - len(line.lstrip())) / INDENTATION_AMOUNT for line in question['solution']]

    order_correct = all([question['scramble_order'][val] == i for i, val in enumerate(given_order)])
    indentation_correct = given_indentation == correct_indentation

    if order_correct and indentation_correct:
        return True

    if 'test_cases' not in question:
        return False

    return run_test_cases(question, given_order, given_indentation)

@app.route('/question/<question_id>', methods=['POST'])
@login_required
def answer_question(question_id):
    question = get_question_from_id(question_id)
    if not question:
        return 'Question not found', 404

    given_order = json.loads(request.form.get('order', '[]'))
    given_indentation = json.loads(request.form.get('indentation', '[]'))

    return RESPONSE_SUCCESS if check_answer(question, given_order, given_indentation) else RESPONSE_FAILED
