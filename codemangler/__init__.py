from flask import Flask

from config import MongoConfig, Config

app = Flask(__name__, static_url_path='')
app.secret_key = Config.SECRET_KEY
db = MongoConfig.db

# run app view from users, questions and admin #
from codemangler.views import users, questions, admin
