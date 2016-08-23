#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from file_storage.routes import Routes
from file_storage.controllers.home import app as home_app


def create_app():
    app = Bottle()
    app.merge(Routes)
    app.tokens = home_app.tokens
    return app
