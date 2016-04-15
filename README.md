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



## Additional Resources
