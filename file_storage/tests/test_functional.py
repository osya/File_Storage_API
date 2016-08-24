#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime as dt


# # noinspection PyClassHasNoInit
# class TestRegistering:
#
#     def test_register_with_real_ip(self, test_app, test_ip):
#         res = test_app.get('/register', {'ip': test_ip[0]})
#         assert 200 == res.status_code
#         token = res.json['Token']
#         assert token is not None
#
#     def test_register_with_empty_ip(self, test_app):
#         res = test_app.get('/register', {'ip': ''}, expect_errors=True)
#         assert 400 == res.status_code
#
#         res = test_app.get('/register', expect_errors=True)
#         assert 400 == res.status_code


# noinspection PyClassHasNoInit
class TestUploadFile:
    # def test_upload_file_with_correct_token(self, test_app, test_ip):
    #     with open('README.rst', 'rb') as f:
    #         res = test_app.post(
    #                 '/upload',
    #                 {
    #                     'token': test_ip[1],
    #                     'expired_date': dt.datetime.now().date()
    #                 },
    #                 upload_files=[('upload', 'README.rst', f.read())])
    #     assert 200 == res.status_code

    def test_upload_file_with_wrong_expired_date(self, test_app, test_ip):
        res = test_app.post('/upload', {'token': test_ip[1], 'expired_date': ''}, expect_errors=True)
        assert 400 == res.status_code
        res = test_app.post('/upload', {'token': test_ip[1]}, expect_errors=True)
        assert 400 == res.status_code

    def test_upload_file_with_expired_token(self, test_app, test_ip):
        delay = int(float(test_app.app.tokens[test_ip[1]]['Expiry']) - time.time() + 0.5)
        time.sleep(delay)
        res = test_app.post('/upload', {'token': test_ip[1]}, expect_errors=True)
        assert 403 == res.status_code

    def test_upload_file_with_wrong_token(self, test_app):
        res = test_app.post('/upload', {'token': ''}, expect_errors=True)
        assert 403 == res.status_code
        res = test_app.post('/upload', expect_errors=True)
        assert 403 == res.status_code
