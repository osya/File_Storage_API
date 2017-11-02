# File Storage API

[![Build Status](https://travis-ci.org/osya/File_Storage_API.svg)](https://travis-ci.org/osya/File_Storage_API) [![Coverage Status](https://coveralls.io/repos/github/osya/File_Storage_API/badge.svg?branch=master)](https://coveralls.io/github/osya/File_Storage_API?branch=master)

File storage (HTTP storage) API with IP Auth based on Bottle & SQLite

Developed File storage (HTTP storage) API with IP Auth based on Bottle & SQLite. 

In the scope of this task I developed Bottle plugin for IP Auth, which can work with 
Bottle-SQLite plugin. 

This project uses `multiprocessing` module for removing 
expired uploaded files in background in separate process. 

For testing PyTest & Webtest used.

## Installation
1. Clone project on your machine
2. ```bash virtualenv env```
3. Activate virtual env:
* Under Windows: ```bash env\Scripts\activate.bat```
* Under Linux: ```bash source env/bin/activate```
4. pip install -r requirements/dev.txt
5. cd <path_where_you_cloned_app>
6. ```bash nohup python manage.py runserver```

## Tests
```bash python manage.py test```

## Usage
See in tests
