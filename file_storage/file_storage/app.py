#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle
from file_storage.routes import Routes


def create_app():
    app = Bottle()
    app.merge(Routes)

    return app
