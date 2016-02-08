from flask import Flask, request, render_template
from pymongo import MongoClient

import os
import json

app = Flask(__name__, static_url_path='', template_folder='tmpl/')

def get_collection(db_name, collections):
    server = 'ds059375.mongolab.com'
    port = 59375
    username = 'tanjid'
    password = 'pwd123'
    client = MongoClient(server, port)
    db = client[db_name]
    db.authenticate(username, password, mechanism='SCRAM-SHA-1')
    posts = db[collections]
    question = posts.find()
    data = []
    for item in question:
        data.append(item)
    return data

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

@app.route('/')
def get_questions():
    data = get_collection("code_mangler", "questions")
    #data = get_collection_local("question_db", "questions")
    return render_template('questions.html', questions=data)

@app.route('/question/<question_id>', methods=['GET'])
def get_question(question_id):
    data = get_collection("code_mangler", "questions")[int(question_id)-1]
    #data = get_collection_local("question_db", "questions")
    solution = data['solution']
    scramble_order = data['scramble_order']
    return render_template(
        'question.html',
        id=data['id'],
        question=data['question'],
        description=data['description'],
        lines=[solution[i].lstrip() for i in scramble_order]
    )

@app.route('/question/<question_id>', methods=['POST'])
def answer_question(question_id):

    ans = json.loads(request.form.get('answer', '[]'))
    data = get_collection("code_mangler", "questions")[int(question_id)-1]
    return 'Correct' if ans == data['scramble_order'] else 'Try Again'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    # Setting up local server for Flask
    app.debug = True
    app.run(port=port)
