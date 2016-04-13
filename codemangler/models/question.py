from config import MongoConfig


class Question(object):
    def __init__(self, _id, question, solution, scramble_order, test_cases, input_description, output_description,
                 category, difficulty, attempts=0, success=0):
        self._id = _id
        self.question = question
        self.solution = solution
        self.scramble_order = scramble_order
        self.test_cases = test_cases
        self.input_description = input_description
        self.output_description = output_description
        self.category = category
        self.difficulty = difficulty
        self.attempts = attempts
        self.success = success


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
            'difficulty': self.question.difficulty,
            'attempts': self.question.attempts,
            'success': self.question.success
        }

        table = MongoConfig.question
        table.insert(question_data)


class UpdateQuestion:
    def __init__(self, question):
        self.question = question

    def post(self):
        table = MongoConfig.question
        question_data = {
            'question': self.question.question,
            'solution': self.question.solution,
            'scramble_order': self.question.scramble_order,
            'test_cases': self.question.test_cases,
            'input_description': self.question.input_description,
            'output_description': self.question.output_description,
            'category': self.question.category,
            'difficulty': self.question.difficulty,
            'attempts': self.question.attempts,
            'success': self.question.success
        }
        table.update_one(
            {'_id': self.question._id},
            {'$set': question_data}
        )
        return GetQuestion(self.question._id).get()


class GetQuestion:
    def __init__(self, _id):
        self._id = _id

    def get(self):
        question = MongoConfig.question.find_one({'_id': self._id})
        return Question(
            question['_id'],
            question['question'],
            question['solution'],
            question['scramble_order'],
            question['test_cases'],
            question['input_description'],
            question['output_description'],
            question['category'],
            question['difficulty'],
            question['attempts'],
            question['success']
        )
