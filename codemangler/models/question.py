from config import MongoConfig


class Question(object):
    def __init__(self, qid, question, solution, scramble_order, test_cases, input_description, output_description,
                 category, difficulty):
        self._id = qid
        self.question = question
        self.solution = solution
        self.scramble_order = scramble_order
        self.test_cases = test_cases
        self.input_description = input_description
        self.output_description = output_description
        self.category = category
        self.difficulty = difficulty


class CreateQuestion:
    def __init__(self, question):
        self.question = question

    def populate(self):
        question_data = {
            'question': self.question.question,
            'solution': self.question.solution,
            'scramble_order': self.question.scramble_order,
            'test_cases': self.question.test_cases,
            'input_description': self.question.input_description,
            'output_description': self.question.output_description,
            'category': self.question.category,
            'difficulty': self.question.difficulty
        }

        table = MongoConfig.question
        table.insert(question_data)


class PostQuestion:
    def __init__(self, qid, data):
        self.qid = qid
        self.data = data

    def post(self):
        table = MongoConfig.question
        table.update_one(
            {'_id': self.qid},
            {'$set': self.data}
        )
        return GetQuestion(self.qid).get()


class GetQuestion:
    def __init__(self, qid):
        self.qid = qid

    def get(self):
        question = MongoConfig.question.find_one({'_id': self.qid})
        return Question(
            question['_id'],
            question['question'],
            question['solution'],
            question['scramble_order'],
            question['test_cases'],
            question['input_description'],
            question['output_description'],
            question['category'],
            question['difficulty']
        )
