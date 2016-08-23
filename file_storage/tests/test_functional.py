#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from webtest import TestApp
from file_storage.app import create_app


class TestRegistering(unittest.TestCase):

    def test_get_token(self):
        app = TestApp(create_app())
        res = app.get('/get_token', {'ip': '127.0.0.1'})
        assert 200 == res.status_code
        token = res.json_body['Token']
        assert token is not None


# def test_functional_login_logout():
#     app = TestApp(file_storage.app)
#
#     app.post('/login', {'user': 'foo', 'pass': 'bar'}) # log in and get a cookie
#
#     assert app.get('/admin').status == '200 OK'        # fetch a page successfully
#
#     app.get('/logout')                                 # log out
#     app.reset()                                        # drop the cookie
#
#     # fetch the same page, unsuccessfully
#     assert app.get('/admin').status == '401 Unauthorized'


# def test_functional_index():
#     assert file_storage.index() == 'Hi!'
