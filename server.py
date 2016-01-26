from flask import Flask, jsonify, request, abort, render_template
from mongoengine import connect

import models
import logic
import os

app = Flask(__name__, static_url_path='', template_folder='tmpl/')

connect('codemangler', host='localhost', port=27017)


@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/login', methods=['GET'])
def login():
    return '<form method="get" action="/login"><input type="text" name="username" />' \
           '<buttom type="submit">Submit</button></form>'

@app.route('/question', methods=['GET'])
def get_question():
    # For now the return data is hardcoded
    temp = [{'topic': 'For Loops'},
            {'lines': ['for w in words', 'print(w)']}]
    response = jsonify(result=temp)
    return response


@app.route('/question', methods=['POST'])
def post_question():
    fields = ['topic', 'lines']
    parsed_data = request.get_json(silent=True)

    if logic.isFieldsExist(parsed_data, fields):
        question_topic = parsed_data.get('topic')
        code_lines = parsed_data.get('lines').split(',')
        new_question = Question(topic=question_topic, lines=code_lines).save()
        return jsonify(result=str(new_question.id))
    else:
        abort(422)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.debug = True
    app.run(port=port)
