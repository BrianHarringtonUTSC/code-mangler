from collections import namedtuple
from flask import Flask, jsonify, request, abort, render_template

import os
import json
import re

app = Flask(__name__, static_url_path='', template_folder='tmpl/')

Question = namedtuple('Question', 'id question solution scramble_order')

answer_regex = re.compile('^((\s*[0-9]+),)*(\s*[0-9]+)$')

# hardcoded data for now. TODO: add DB
data = Question(1, 'Calculate the sum of a list of numbers.',
                ['def sum(L):', '  sum = 0', '  for item in L:', '    sum += item', '  return sum'],
                [4, 1, 2, 3, 0])

@app.route('/')
def get_questions():
    return render_template('questions.html', questions=[data])

@app.route('/question/<question_id>', methods=['GET'])
def get_question(question_id):
    lines = [data.solution[i].lstrip() for i in data.scramble_order]
    return render_template('question.html', id=data.id, question=data.question, lines=lines)

@app.route('/question/<question_id>', methods=['POST'])
def answer_question(question_id):
    ans = json.loads(request.form.get('answerLine', []))
    return 'Correct' if ans == data.scramble_order else 'Try Again'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(port=port)
