from flask import Flask
from flask.ext.mongoengine import MongoEngine
app = Flask(__name__,static_url_path='')

# Setup connection with MongoDB
dbSettings = {'db':'codemangler', 'host':'localhost', 'port':27017}
app.config["MONGODB_SETTINGS"] = dbSettings
db = MongoEngine(app)

@app.route('/')
def root():
	return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(port=8000)
