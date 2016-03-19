from flask import Flask
from pymongo import MongoClient


app = Flask(__name__, static_url_path='')
app.secret_key = "my precious"

DB_URI = 'mongodb://tanjid:pwd123@ds059375.mlab.com:59375/code_mangler'
client = MongoClient(DB_URI)
db = client.code_mangler

from codemangler import views
