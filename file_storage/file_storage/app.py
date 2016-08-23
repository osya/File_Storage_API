#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beaker.middleware import SessionMiddleware
from bottle import Bottle
from file_storage.routes import Routes


def create_app():
    session_opts = {
        'session.type': 'file',
        'session.auto': True
    }

    app = SessionMiddleware(Bottle(), session_opts)

    # Bottle Routes
    app.wrap_app.merge(Routes)

    return app
