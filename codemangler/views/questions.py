import json
import os
import subprocess
import tempfile
from math import ceil

from bson import ObjectId
from flask import request, render_template, session

from codemangler import app, db
from codemangler.models.question import GetQuestion, UpdateQuestion
from codemangler.models.user import GetUser, UpdateUser
from codemangler.views.users import login_required

INDENTATION_AMOUNT = 4
RESPONSE_SUCCESS = 'Correct'
RESPONSE_FAILED = 'Try Again'


@app.route('/')
@login_required
def get_questions():
    """ () -> rendered_template

    Returns the rendered template of questions.html with data from list
    of Question objects, after the user makes a GET request to to home page
    """
    if 'logged_in' in session and 'username' in session:
        user = GetUser(session['username']).get()
    questions = db.questions.find()
    unattempted = questions.count() - len(user.completed)
    return render_template('questions.html',
                           questions=questions,
                           completed=user.completed,
                           unattempted=unattempted,
                           user=user)


@app.route('/question/<question_id>', methods=['GET'])
@login_required
def get_question(question_id):
    """ (str) -> rendered_template

    Returns the rendered template of question.html with data from the
    Question objects, after the user makes a GET request to to question page
    """
    question = GetQuestion(ObjectId(question_id)).get()
    if not question:
        return 'Question not found', 404

    solution = question.solution
    scramble_order = question.scramble_order
    session["try"] = 0
    return render_template('question.html', question=question,
                           lines=[solution[i].lstrip() for i in scramble_order])


def run_test_cases(question, given_order, given_indentation):
    """ (str, list of int, list of int) -> Boolean

    Returns True if test cases return True, else False
    """
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
    """ (Question, list of int, list of int) -> Boolean

    Return True if test cases are ran successfully, otherwise, False
    """
    correct_indentation = [int(len(line) -
                               len(line.lstrip())) / INDENTATION_AMOUNT for line in question.solution]

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
    """ (str) -> str

    Return success message if answer is correct,
    Otherwise return the failure message
    """
    session["try"] += 1
    question = GetQuestion(ObjectId(question_id)).get()

    if not question:
        return 'Question not found', 404

    given_order = json.loads(request.form.get('order', '[]'))
    given_indentation = json.loads(request.form.get('indentation', '[]'))

    user = GetUser(session["username"]).get()

    if ObjectId(question_id) not in user.completed:
        question.attempts += 1

    if check_answer(question, given_order, given_indentation):
        if ObjectId(question_id) not in user.completed:
            user.completed.append(ObjectId(question_id))
            if session["try"] > 10:
                user.xp += question.difficulty
            else:
                user.xp += ceil(int(question.difficulty) * 10 / int(session["try"]))
            user.level = ceil(user.xp / 25)
            question.success += 1
        UpdateQuestion(question).post()
        UpdateUser(user).post()
        session.pop("try", None)
        return RESPONSE_SUCCESS + "<br>Return to home for more challenges"
    else:
        return RESPONSE_FAILED + "<br>Failed Attempt: " + str(
            session["try"]) + "<br>More failed attempts results in less trophies"
