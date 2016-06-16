from datetime import datetime

from codemangler import bcrypt
from config import MongoConfig


class User(object):
    """ A User Object """

    def __init__(self, username, name, email, _id=None, user_type="regular", attempted=[],
            completed=[], xp=0, level=0, account_created=None, last_modified=None):
        """ (User, str, str, str, str, str, ObjectId(), str, Boolean, List of ObjectId(),
        List of ObjectId(), int, int, datetime, datetime) -> NoneType

        A new User with necessary username, password, first and last name, unique id, user type, activeness,
        attempted and completed questions, trophies/xp, level, data of creating and last modifying account

        id must be ObjectId() when it is a new user, for creating an instance of User to add to the DB
        """
        self.username = username
        self.name = name
        self.email = email
        self._id = _id
        self.user_type = user_type
        self.attempted = attempted
        self.completed = completed
        self.xp = xp
        self.level = level
        self.account_created = account_created
        self.last_modified = last_modified

class UserModel(object):

    def get(filter_or_id):
        """ (dict or bson.ObjectId) -> User

        Return the instance of User object associated with the user data
        """
        doc = MongoConfig.user.find_one(filter_or_id)
        if not doc:
            return None

        return User(
            doc['username'],
            doc['name'],
            doc['email'],
            doc['_id'],
            doc['user_type'],
            doc['attempted'],
            doc['completed'],
            doc['xp'],
            doc['level'],
            doc['account_created'],
            doc['last_modified'])

    def create(user):
        """ (User) -> NoneType

        Convert data from the instance of User object into a Dictionary/JSON

        Populate questions collection with the data from dictionary, in other words,
                 create a new entry with the dictionary user_data
        """
        user.account_created = str(datetime.now())[:16]
        user.last_modified = str(datetime.now())[:16]
        result = MongoConfig.user.insert_one(user.__dict__)
        if result:
            return UserModel.get(result.inserted_id)

    def update(user):
        """ (User) -> User

        Update database entry with data associated with User
                Then return the updated object from the database
        """
        user.last_modified = str(datetime.now())[:16]

        # Update user entry if username matches #
        MongoConfig.user.update_one(
            {'username': user.username},
            {'$set': user.__dict__}
        )
        return UserModel.get(user.username)
