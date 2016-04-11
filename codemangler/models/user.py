from datetime import datetime

from codemangler import bcrypt
from config import MongoConfig


class User(object):
    def __init__(
            self, username, password, first_name, last_name, email,
            _id=None, user_type="regular", active=False, attempted=[],
            completed=[], xp=0, level=0):
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


class Create:
    def __init__(self, user):
        self.user = user

    def populate(self):
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

        table = MongoConfig.user
        table.insert(user_data)


class Post:
    def __init__(self, username, data):
        self.username = username
        self.data = data

    def post(self):
        table = MongoConfig.user
        self.data['lastModified'] = str(datetime.now())[:16]
        table.update_one(
            {'username': self.username},
            {'$set': self.data}
        )
        return Get(self.username).get()


class Get:
    def __init__(self, username):
        self.username = username

    def get(self):
        user = MongoConfig.user.find_one({'username': self.username})
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
            user['level'])
