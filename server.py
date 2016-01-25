from flask import Flask
from flask.ext.mongoengine import MongoEngine

# Initialize Flask
app = Flask(__name__, static_url_path='')
# Setup connection with MongoDB
app.config["MONGODB_SETTINGS"] = {"DB": "localhost:27017"}
db = MongoEngine(app)

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/question', methods = ['GET', 'POST', 'DELETE'])
def api_question():
	if request.method == 'GET':
		return 'GET\n';
	elif request.method == 'POST':
		return 'POST\n'
	elif request.method == 'DELETE':
		return 'DELETE\n'

if __name__ == '__main__':
    app.run(port=8000)
