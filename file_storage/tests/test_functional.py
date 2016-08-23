#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from webtest import TestApp
from file_storage.app import create_app


class TestRegistering(unittest.TestCase):

    def test_get_token_with_real_ip(self):
        app = TestApp(create_app())
        res = app.get('/get_token', {'ip': '127.0.0.1'})
        self.assertEqual(res.status_code, 200)
        token = res.json['Token']
        assert token is not None

    def test_get_token_with_empty_ip(self):
        app = TestApp(create_app())
        res = app.get('/get_token', {'ip': ''}, expect_errors=True)
        self.assertEqual(res.status_code, 400)

        app = TestApp(create_app())
        res = app.get('/get_token', expect_errors=True)
        self.assertEqual(res.status_code, 400)


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
