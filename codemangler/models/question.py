from config import MongoConfig

# TODO: fix this to match user model
class Question(object):
    """ A Question Object """

    def __init__(self, _id, question, solution, scramble_order, test_cases, input_description, output_description,
                 category, difficulty, attempts=0, success=0):
        """ (Question, ObjectId(), str, list of str, list of int, list of str,
                str, str, list of str, int, int, int) -> NoneType

        A new Question with necessary data like unique id, question title, solution as code, order of scramble, test cases,
        input and out description, categories, difficulties and number of user attempts/successes

        id must be ObjectId() when it is a new question, for creating an instance of Question to add to the DB
        """
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
    """ Takes question data as Question object into a dictionary
    then populates dictionary into the database question """

    def __init__(self, question):
        """ (CreateQuestion, Question) -> NoneType

        Initializes a new Question object
        """
        self.question = question

    def populate(self):
        """ (CreateQuestion) -> NoneType

        Convert data from the instance of Question object into a Dictionary/JSON

        Populate questions collection with the data from dictionary, in other words,
                 create a new entry with the dictionary question_data
        """
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
        # Connect to the question collection
        # Then insert question_data as an entry
        table = MongoConfig.question
        table.insert(question_data)


class UpdateQuestion:
    """ Takes Question data and updates existing question associated with the data """

    def __init__(self, question):
        """ (UpdateQuestion, Question) -> NoneType

        Initializes updated Question data
        """
        self.question = question

    def post(self):
        """ (UpdateQuestion) -> Question

        Update database entry with data associated with Question
                Then return the updated object from the database
        """
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
        # Update question entry if _id matches #
        table.update_one(
            {'_id': self.question._id},
            {'$set': question_data}
        )
        return GetQuestion(self.question._id).get()


class GetQuestion:
    """ Takes Question id and returns the associated Question data
    from the database as an instance of the Question object """

    def __init__(self, _id):
        """ (GetQuestion, ObjectId()) -> NoneType

        Initialize unique id for the question
        """
        self._id = _id

    def get(self):
        """ (GetQuestion) -> Question

        Return the Question object associated with the _id from the database
        """
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
