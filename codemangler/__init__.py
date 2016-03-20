from flask import Flask
from config import MongoConfig, Config
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, static_url_path='')
bcrypt = Bcrypt(app)
app.secret_key = Config.SECRET_KEY
db = MongoConfig.db

from codemangler import views
