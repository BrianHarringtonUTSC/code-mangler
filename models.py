from mongoengine import *

class User(Document):
    name = StringField(max_length=50, required=True)
    utorid = StringField(max_length=10, required=True)

class Question(Document):
    topic = StringField(max_length=50, required=True)
    lines = ListField(StringField(required=True))
