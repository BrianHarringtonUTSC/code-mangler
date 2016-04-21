# Code Mangler
Code Mangler is an application for beginner programmers to get a better understanding of Python programming language. 


### Features
- User Accounts (Login & Registration)
- Questions List by Categories
- Questions seperated by Completed and Uncompleted
- Tracking User Achievements & Stats
- Tracking Question Stats
- Reorganizing and Indenting to Solve Mangled Up Code
- Admin Side
    - Uploading Questions
    - Running Test Cases for each Question
    - Managing and Deleting Questions
    - Managing and Deleting Users
    - Giving other Users Admin Access


### Requirements
- Python 3.5.1 (https://www.python.org/downloads/)
- Flask 0.10.1 (http://flask.pocoo.org/)
- Flask-Bcrypt 0.6.0 (https://flask-bcrypt.readthedocs.org/en/latest/)
- Flask-PyMongo 0.4.1 (https://flask-pymongo.readthedocs.org/en/latest/)
- MongoDB 3.2 (https://www.mongodb.org/)


### Code Mangler Quick Start Guide

This guide will walk you through deploying Code Mangler locally and tracademic server.

#### Usage

```console
$ git clone https://github.com/TanjidIslam/code-mangler.git
$ cd code-mangler
$ pyvenv-3.5 env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

#### To run on local server
```console
$ python3 localserver.py
```

#### To run on tracademic server
```console
$python3 runserver.py
```

### TODO
- HTTPS: Security against DDos, Fraud, etc
- Tracking User Attempts: Code States
- Social Network OAuth (http://pythonhosted.org/Flask-Social/)
- User: Edit Profile (Same as Admin's functionality of editing user profiles)


### Design Choices
Design choices are as important as application implementations. In this section, I will demonstrate on my choice of design and tools and point out how they connect.
I used Model-View-Controller pattern, also known as the famous MVC pattern. I chose Python with Flask framework because it is light and gives me the freedom to use <b>routes, models, views & controllers</b>, the 4 major components of MVC pattern.

#### Routes
A user <b>requests</b> to view a page by entering a URL:
```HTML
http://codemangler.utoronto.ca/login
```

The application matches the URL pattern with a predefined <b>route</b>:
```
    http://codemangler.utoronto.ca/'login'
```

With each <b>route</b> is associated with a controller, more specifically a certain function within the controller, also known as the <b>controller action</b>:
```python
@app.route('/login')
def login():
    #doSomething
```

#### Models and Controllers
The <b>controller action</b> uses the models (user or question model for this case) to retrieve all of the necessary data from a database, places the data in a data structure (dictionary/json in this case), and loads a view, passing along the data structure:
```python
@app.route('/login', methods=['GET'])
def login_user():
    user_list = MongoConfig.users       # All user entries in a dictionary
    ..
    ..
    if request.form["username"] in user_list:
        current_user = user_list[request.form["username"]]
    return render_template('questions.html', current_user)


Class MongoConfig:
    DB_URI = ...
    client = MongoClient(DB_URI)
    db = client.collection
    users = db.accounts
    questions = db.questions
```

#### Views
The <b>view</b>, the basic structure of data that was passed on by <b>controller action</b>, uses it to render the requested page, which is then displayed to the user in their browser.
```jinja2
{% for question in questions %}
  <li>
    <h2>{{ question.title }}</h2>
    <div>{{ question.description }}</div>
  </li>
{% else %}
  <li><em>No questions in the database!</em></li>
{% endfor %}
```


### Project Structure
Based on (http://flask.pocoo.org/docs/0.10/patterns/packages/)

    - Codemangler
        - models
            - question.py
            - user.py
        
        - views
            - admin.py
            - questions.py
            - users.py
        
        - templates
            - admin.html
            - admin-question.html
            - admin-questions.html
            - admin-user.html
            - admin-users.html
            - base.html
            - footer.html
            - head.html
            - head-question.html
            - jslibadmin.html
            - jslibraries.html
            - jslibraries-question.html
            - login.html
            - navbar.html
            - navbar-admin.html
            - question.html
            - questions.html
            - signup.html
            - upload.html
       
        - static
            - bootstrap/..
            - css/..
            - font-awesome/..
            - img/..
            - js/..
    
    
    - __init__.py
    - config.py
    - requirements.txt
    - localserver.py
    - runserver.py



### Project Context
        Codemangler - contains models, views, templates, and front-end files (css, javascript, jqeuery, ajax)
    
            models - This is where models are defined, contains user and question structures, 
            that can be used to create, update and get database entries for user accounts and questions
            
            views - This is where routes are defined, contains all view functions with route() decorator
            
            templates - This is where Jinja2 templates are defined, contains all pages files that routes communicate with
            
            static - This is where all the front-end files are defined, contains all static that do not change and 
            are used for user side
            
            
        __init__.py - This file initializes the application and brings together all of the various components
        
        
        config.py - This is where all the configuration variables are defined, contains variables like secret keys and database access
        
        
        requirements.txt - This file lists all of the Python packages that the application depends on
        
        
        run
            localserver.py - Run this application to deploy it on local server (http://127.0.0.1:8000)
            
            runserver.py - Run this application to deploy it on tracademic server (http://142.1.97.144:5000/)
        
        
        
        
