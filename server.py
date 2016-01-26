from flask import Flask, jsonify, request, abort
from mongoengine import connect
from models import *
from logic import *
import os

# Initialize Flask
app = Flask(__name__, static_url_path='')

# Setup MongoDB connection
connect('codemangler', host='localhost', port=27017)


@app.route('/')
def hello_world():
    hello2()
    return "Hello World"

def hello2():
    return "After Hello World"

def root():
    return app.send_static_file('index.html')


@app.route('/question', methods=['GET'])
def get_question():
    # For now the return data is hardcoded
    temp = [{'topic': 'For Loops'},
            {'lines': ['for w in words', 'print(w)']}]
    # Jsonify and return the data
    response = jsonify(result=temp)
    return response


@app.route('/question', methods=['POST'])
def post_question():
    # Parse data and define fields to check
    fields = ['topic', 'lines']
    parsed_data = request.get_json(silent=True)
    # Check if request data is valid
    if isFieldsExist(parsed_data, fields):
        # Obtain the topic and code lines from the parsed data
        question_topic = parsed_data.get('topic')
        code_lines = parsed_data.get('lines').split(',')
        # Store as a new document in the database and return id of new entry
        new_question = Question(topic=question_topic, lines=code_lines).save()
        return jsonify(result=str(new_question.id))
    else:
        abort(422)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(debug=True, port=port)
