from functools import wraps
from random import shuffle

from bson import ObjectId
from flask import request, render_template, session, redirect, url_for

from codemangler import app, db
from codemangler.models.question import Question, CreateQuestion
from codemangler.models.user import GetUser
from config import MongoConfig


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session)
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            return 'No Access', 403

    return wrap


@app.route('/admin', methods=['GET'])
@admin_required
def get_admin():
    return render_template('admin.html')


@app.route('/admin/students', methods=['GET'])
@admin_required
def get_student_list():
    users = db.accounts.find()
    return render_template('admin-student.html', users=users)


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
