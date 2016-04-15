# Code Mangler Quick Start Guide

This guide will walk you through deploying Code Mangler locally and tracademic server.

## Requirement

Download Python 3.5: (https://www.python.org/downloads/)

## Usage

```console
$ git clone https://github.com/TanjidIslam/code-mangler.git
$ cd code-mangler
$ pyvenv-3.5 env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

### To run locally
```console
$ python3 localserver.py
```

###To run on tracademic
```console
$python3 runserver.py
```

## Project Structure
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



## Project Context

        Codemangler - contains models, views, templates, and front-end files (css, javascript, jqeuery, ajax)
    
            models - This is where models are defined, contains user and question structures, that can be used to create, update and get database entries for user accounts and questions
            
            views - This is where routes are defined, contains all view functions with route() decorator
            
            templates - This is where Jinja2 templates are defined, contains all pages files that routes communicate with
            
            static - This is where all the front-end files are defined, contains all static that do not change and are used for user side
            
            
        __init__.py - This file initializes the application and brings together all of the various components
        
        
        config.py - This is where all the configuration variables are defined, contains variables like secret keys and database access
        
        
        requirements.txt - This file lists all of the Python packages that the application depends on
        
        
        run
            localserver.py - Run this application to deploy it on local server (http://127.0.0.1:8000)
            
            runserver.py - Run this application to deploy it on tracademic server (http://142.1.97.144:5000/)
        
        
        
        
