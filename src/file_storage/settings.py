# -*- coding: utf-8 -*-
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(PROJECT_PATH)), 'static')
TEST_PATH = os.path.join(os.path.dirname(PROJECT_PATH), 'tests')
SQLITE_FILE_NAME = 'db.sqlite'
