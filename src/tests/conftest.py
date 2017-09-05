#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import datetime as dt
import os

import pytest
from webtest import TestApp

from file_storage import settings
from file_storage.controllers.api import app as api


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    yield api


@pytest.fixture(scope='function')
def test_app(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture
def test_ip(app):
    """A user for the tests."""
    ip = '127.0.0.1'
    return ip, app.tokens.add(ip)


@pytest.fixture
def file_key(test_app, test_ip):
    with open(os.path.join(settings.TEST_PATH, 'README.rst'), 'rb') as f:
        res = test_app.post(
            '/upload',
            {
                'token': test_ip[1],
                'expired_date': dt.datetime.utcnow().date()
            },
            upload_files=[('upload', 'README.rst', f.read())])
        return res.json['Key']
