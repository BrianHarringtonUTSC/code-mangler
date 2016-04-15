from datetime import datetime

from codemangler import bcrypt
from config import MongoConfig


class User(object):
    """ A User Object """

    def __init__(
            self, username, password, first_name, last_name, email,
            _id=None, user_type="regular", active=False, attempted=[],
            completed=[], xp=0, level=0, accountCreated=None, lastModified=None):
        """ (User, str, str, str, str, str, ObjectId(), str, Boolean, List of ObjectId(),
        List of ObjectId(), int, int, datetime, datetime) -> NoneType

        A new User with necessary username, password, first and last name, unique id, user type, activeness,
        attempted and completed questions, trophies/xp, level, data of creating and last modifying account

        id must be ObjectId() when it is a new user, for creating an instance of User to add to the DB
        """
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._id = _id
        self.user_type = user_type
        self.active = active
        self.attempted = attempted
        self.completed = completed
        self.xp = xp
        self.level = level
        self.accountCreated = accountCreated
        self.lastModified = lastModified


class CreateUser:
    """ Takes user data as User object into a dictionary
     then populates dictionary into the database user """

    def __init__(self, user):
        """ (CreateUser, User) -> NoneType

        Initializes a new User object
        """
        self.user = user

    def populate(self):
        """ (CreateUser) -> NoneType

        Convert data from the instance of User object into a Dictionary/JSON

        Populate questions collection with the data from dictionary, in other words,
                 create a new entry with the dictionary user_data
        """
        self.user.active = True
        user_data = {
            'username': self.user.username,
            'password': bcrypt.generate_password_hash(self.user.password),
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'user_type': self.user.user_type,
            'active': self.user.active,
            'attempted': self.user.attempted,
            'completed': self.user.completed,
            'xp': self.user.xp,
            'level': self.user.level,
            'accountCreated': str(datetime.now())[:16],
            'lastModified': str(datetime.now())[:16]
        }
        # Connect to the question collection #
        # Then insert question_data as an entry #
        table = MongoConfig.user
        table.insert(user_data)


class UpdateUser:
    """ Takes User data and updates existing user associated with the data """

    def __init__(self, user):
        """ (UpdateUser, User) -> NoneType

        Initializes updated User data
        """
        self.user = user

    def post(self):
        """ (UpdateUser) -> User

        Update database entry with data associated with User
                Then return the updated object from the database
        """
        table = MongoConfig.user
        self.user.lastModified = str(datetime.now())[:16]
        user_data = {
            'username': self.user.username,
            'password': self.user.password,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'user_type': self.user.user_type,
            'active': self.user.active,
            'attempted': self.user.attempted,
            'completed': self.user.completed,
            'xp': self.user.xp,
            'level': self.user.level,
            'accountCreated': self.user.accountCreated,
            'lastModified': self.user.lastModified
        }
        # Update user entry if username matches #
        table.update_one(
            {'username': self.user.username},
            {'$set': user_data}
        )
        return GetUser(self.user.username).get()


class GetUser:
    """ Takes user id or username and returns the associated User data
    from the database as an instance of the User object """

    def __init__(self, data):
        """ (GetUser, ObjectId() or Str) -> NoneType

        Initialize unique user data for the user
        """
        self.data = data

    def get(self):
        """ (GetUser) -> User

        Return the instance of User object associated with the user data
        """
        if MongoConfig.user.find_one({'username': self.data}):
            user = MongoConfig.user.find_one({'username': self.data})
        elif MongoConfig.user.find_one({'_id': self.data}):
            user = MongoConfig.user.find_one({'_id': self.data})
        return User(
            user['username'],
            user['password'],
            user['first_name'],
            user['last_name'],
            user['email'],
            user['_id'],
            user['user_type'],
            user['active'],
            user['attempted'],
            user['completed'],
            user['xp'],
            user['level'],
            user['accountCreated'],
            user['lastModified']
        )
