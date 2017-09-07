#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import datetime as dt
import os
import sqlite3
import tempfile

import pytest
from bottle_sqlite import SQLitePlugin
from webtest import TestApp

from file_storage import settings
from file_storage.bottle_ipauth import IPAuthPlugin, TokenManager
from file_storage.controllers.api import api as _app


@pytest.yield_fixture(scope='session')
def app():
    """An application for the tests."""
    yield _app


@pytest.fixture(scope='session')
def test_ip():
    ip = '127.0.0.1'
    return ip


@pytest.yield_fixture(scope='session')
def test_app(app, test_ip):
    """A Webtest app."""

    app.install(IPAuthPlugin(token_manager=TokenManager()))

    # It is not possible to use in-memory SQLite for testing. Because for every new connection table schema will be
    # empty. So temp file will be used for test database
    fd, dbfile = tempfile.mkstemp(suffix='.sqlite')
    sqlite_plugin = app.install(SQLitePlugin(dbfile=dbfile))
    # Create database
    with sqlite3.connect(dbfile) as conn:
        conn.execute('CREATE TABLE access_log\n'
                     '            (\n'
                     '                id INTEGER PRIMARY KEY,\n'
                     '                file_key BLOB,\n'
                     '                access_date DATETIME,\n'
                     '                last_access_date DATETIME\n'
                     '            )')
        conn.commit()

        # Register IP
        t_app = TestApp(app, extra_environ={'REMOTE_ADDR': test_ip})
        res = t_app.get('/register')
        assert 200 == res.status_code
        t_app.token = res.json['Token']
        assert t_app.token is not None

        yield t_app

    # teardown
    if conn:
        conn.close()
    os.close(fd)
    os.unlink(sqlite_plugin.dbfile)


@pytest.fixture
def file_key(test_app):
    with open(os.path.join(os.path.dirname(os.path.dirname(settings.TEST_PATH)), 'README.md'), 'rb') as f:
        res = test_app.post(
            '/upload',
            {
                'token': test_app.token,
                'expired_date': dt.datetime.utcnow().date()
            },
            upload_files=[('upload', 'README.md', f.read())])
        return res.json['Key']
