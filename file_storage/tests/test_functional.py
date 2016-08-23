#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


# noinspection PyClassHasNoInit
class TestRegistering:

    def test_register_with_real_ip(self, test_app, test_ip):
        res = test_app.get('/register', {'ip': test_ip[0]})
        assert 200 == res.status_code
        token = res.json['Token']
        assert token is not None

    def test_register_with_empty_ip(self, test_app):
        res = test_app.get('/register', {'ip': ''}, expect_errors=True)
        assert 400 == res.status_code

        res = test_app.get('/register', expect_errors=True)
        assert 400 == res.status_code


# noinspection PyClassHasNoInit
class TestImportFile:

    def test_import_file_with_correct_token(self, test_app, test_ip):
        res = test_app.get('/import_file', {'token': test_ip[1]})
        assert 200 == res.status_code

    def test_import_file_with_timeout_token(self, test_app, test_ip):
        delay = int(float(test_app.app.tokens[test_ip[1]]['Expiry']) - time.time() + 0.5)
        time.sleep(delay)
        res = test_app.get('/import_file', {'token': test_ip[1]}, expect_errors=True)
        assert 403 == res.status_code

    def test_import_file_with_wrong_token(self, test_app):
        res = test_app.get('/import_file', {'token': ''}, expect_errors=True)
        assert 403 == res.status_code
        res = test_app.get('/import_file', expect_errors=True)
        assert 403 == res.status_code
