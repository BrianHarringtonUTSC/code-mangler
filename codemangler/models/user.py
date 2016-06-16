from datetime import datetime

from codemangler import bcrypt
from config import MongoConfig


class User(object):
    """ A User Object """

    def __init__(self, username, name, email, _id=None, user_type="regular", attempted=[],
            completed=[], xp=0, level=0, account_created=None, last_modified=None):
        """ (User, str, str, str, bson.ObjectId, str, Boolean, List of bson.ObjectId,
        List of bson.ObjectId, int, int, datetime, datetime) -> NoneType

        A new User with necessary username, name, email, unique id, user type, activeness,
        attempted and completed questions, trophies/xp, level, data of creating and last modifying account

        All kwargs can be left untouched for a new user and they will be filled upon creation (by calling User.create).
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
    """UserModel handles interactions with the database."""

    def get(filter_or_id):
        """ (dict or bson.ObjectId) -> User

        Return the instance of User object associated with the filter or id.
        """
        doc = MongoConfig.user.find_one(filter_or_id)
        if not doc:
            return None

        return User(doc['username'],
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
        """ (User) -> User

        Add user to the database.
        """
        user.account_created = str(datetime.now())[:16]
        user.last_modified = str(datetime.now())[:16]
        result = MongoConfig.user.insert_one(user.__dict__)
        return UserModel.get(result.inserted_id)

    def update(user):
        """ (User) -> User

        Update user in the database. Return the updated user.
        """
        user.last_modified = str(datetime.now())[:16]

        # Update user entry if username matches #
        MongoConfig.user.update_one({'username': user.username}, {'$set': user.__dict__})
        return UserModel.get(user.username)
