from pymongo import MongoClient


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'my precious'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class MongoConfig(Config):
    DB_URI = 'mongodb://tanjid:pwd123@ds059375.mlab.com:59375/code_mangler'
    client = MongoClient(DB_URI)
    db = client.code_mangler
    user = db.accounts
    question = db.questions
