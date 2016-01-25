from flask import Flask, jsonify
from flask.ext.mongoengine import MongoEngine

# Initialize Flask
app = Flask(__name__, static_url_path='')
# Setup connection with MongoDB
app.config["MONGODB_SETTINGS"] = {"DB": "localhost:27017"}
db = MongoEngine(app)

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/question', methods = ['GET'])
def api_question():
	# For now the return data is hardcoded
	temp = [{'topic':'For Loops'},
			{'lines':['for w in words','print w, len(w)']}]
	# Jsonify and return the data
	response = jsonify(results=temp)
	return response

if __name__ == '__main__':
    app.run(port=8000)
