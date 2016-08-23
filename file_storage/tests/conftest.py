#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import pytest
from file_storage.app import create_app
from webtest import TestApp


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app()
    yield _app


@pytest.fixture(scope='function')
def test_app(app):
    """A Webtest app."""
    return TestApp(app)
