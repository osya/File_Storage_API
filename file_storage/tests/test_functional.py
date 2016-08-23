#!/usr/bin/env python
# -*- coding: utf-8 -*-
from file_storage.app import create_app
import pytest


# noinspection PyClassHasNoInit
class TestRegistering:

    def test_get_token_with_real_ip(self, test_app):
        res = test_app.get('/get_token', {'ip': '127.0.0.1'})
        assert 200 == res.status_code
        token = res.json['Token']
        assert token is not None

    def test_get_token_with_empty_ip(self, test_app):
        res = test_app.get('/get_token', {'ip': ''}, expect_errors=True)
        assert 400 == res.status_code

        res = test_app.get('/get_token', expect_errors=True)
        assert 400 == res.status_code


# noinspection PyClassHasNoInit
class TestImportFile:

    def test_import_file_with_correct_token(self, test_app):
        res = test_app.get('/get_token', {'ip': '127.0.0.1'})
        res = test_app.get('/import_file', {'token': res.json['Token']})
        assert 200 == res.status_code

    def test_import_file_with_wrong_token(self, test_app):
        res = test_app.get('/import_file', {'token': ''}, expect_errors=True)
        assert 401 == res.status_code
        res = test_app.get('/import_file', expect_errors=True)
        assert 401 == res.status_code
