from functools import wraps
from random import shuffle

from bson import ObjectId
from flask import request, render_template, session, redirect, url_for

from codemangler import app, db
from codemangler.models.question import Question, CreateQuestion, GetQuestion, UpdateQuestion
from codemangler.models.user import GetUser, User, UpdateUser
from config import MongoConfig


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return 'No Access', 403

    return wrap


@app.route('/admin', methods=['GET'])
@admin_required
def get_admin():
    return render_template('admin.html')


@app.route('/admin/users', methods=['GET'])
@admin_required
def get_user_list():
    users = db.accounts.find()
    return render_template('admin-users.html', users=users)


@app.route('/admin/questions', methods=['GET'])
@admin_required
def get_question_list():
    questions = db.questions.find()
    return render_template('admin-questions.html', questions=questions)


@app.route('/admin/user/<user_id>', methods=['GET'])
def view_user(user_id):
    user = GetUser(ObjectId(user_id)).get()
    if not user:
        return 'User not found', 404

    return render_template('admin-user.html', user=user)


@app.route('/admin/question/<question_id>', methods=['GET'])
@admin_required
def view_question(question_id):
    question = GetQuestion(ObjectId(question_id)).get()
    if not question:
        return 'Question not found', 404
    solution = "/r/n".join(question.solution)

    return render_template('admin-question.html', question=question, solution=solution)


@app.route('/admin/user/<user_id>', methods=['POST'])
@admin_required
def edit_user(user_id):
    if request.form['submit'] == 'Save':
        user = GetUser(ObjectId(user_id)).get()
        user.user_type = request.form['user-type'].lower()
        UpdateUser(user).post()
    elif request.form['submit'] == 'Delete':
        db.accounts.remove(ObjectId(user_id))
    return redirect(url_for('get_user_list'))


@app.route('/admin/question/<question_id>', methods=['POST'])
@admin_required
def edit_question(question_id):
    if request.form['submit'] == 'Save':
        question = GetQuestion(ObjectId(question_id)).get()
        question.question = request.form['form-question']
        question.category = request.form['form-category'].split(", ")
        question.solution = request.form['form-solution'].split(", ")
        question.input_description = request.form['form-input']
        question.output_description = request.form['form-output']
        question.test_cases = request.form['form-test'].split(", ")
        question.difficulty = int(request.form['form-difficulty'])
        UpdateQuestion(question).post()
    elif request.form['submit'] == 'Delete':
        db.questions.remove(ObjectId(question_id))
    return redirect(url_for('get_question_list'))


@app.route('/admin/upload')
@admin_required
def upload_page():
    if 'logged_in' in session and 'username' in session:
        user = GetUser(session['username']).get()
    return render_template('upload.html', name=user.first_name + " " + user.last_name)


@app.route('/admin/upload', methods=['POST'])
@admin_required
def upload_code():
    question_check = MongoConfig.question.find({'question': request.form['form-question']}).count() > 0
    if question_check:
        return render_template('upload.html')
    else:

        solution = request.form['form-solution'].split('\r\n')
        solution = list(filter(None, solution))

        scramble_order = list(range(len(solution)))
        shuffle(scramble_order)

        tests = request.form['form-test'].split(', ')
        [x.strip() for x in tests]

        category = request.form['form-category'].split(',')
        [x.strip() for x in category]

        question = Question(
            ObjectId(),
            request.form['form-question'],
            solution,
            scramble_order,
            tests,
            request.form['form-input'],
            request.form['form-output'],
            category,
            request.form['form-difficulty']
        )
        CreateQuestion(question).populate()
        return redirect(url_for('get_questions'))
