#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime as dt
from file_storage import settings
import os
import re


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
class TestUploadDownloadFile:
    def test_upload_file_with_correct_token(self, test_app, test_ip):
        with open('README.rst', 'rb') as f:
            res = test_app.post(
                    '/upload',
                    {
                        'token': test_ip[1],
                        'expired_date': dt.datetime.now().date()
                    },
                    upload_files=[('upload', 'README.rst', f.read())])
        assert 200 == res.status_code

    # def test_download_file_with_correct_token(self, test_app, test_ip):
    #     res = test_app.get('/download', {'token': test_ip[1], 'Key': '1d793e98-fbd5-424f-92d0-28ac6113adea'})
    #     assert 200 == res.status_code
    #
    #     filename = None
    #     for header in res.headerlist:
    #         if type(header) is tuple:
    #             for item in header:
    #                 m = re.search(r'''^.*filename="(.*)"$''', item);
    #                 if m:
    #                     filename = m.group(1)
    #                     break
    #
    #     assert filename
    #
    #     if filename:
    #         file_path = os.path.join(settings.TEST_PATH, filename)
    #         with open(file_path, 'wb') as out_file:
    #             out_file.write(res.body)
    #
    # def test_download_file_with_wrong_key(self, test_app, test_ip):
    #     res = test_app.get('/download', {'token': test_ip[1], 'Key': ''}, expect_errors=True)
    #     assert 400 == res.status_code
    #     res = test_app.get('/download', {'token': test_ip[1]}, expect_errors=True)
    #     assert 400 == res.status_code

    # def test_upload_file_with_wrong_expired_date(self, test_app, test_ip):
    #     res = test_app.post('/upload', {'token': test_ip[1], 'expired_date': ''}, expect_errors=True)
    #     assert 400 == res.status_code
    #     res = test_app.post('/upload', {'token': test_ip[1]}, expect_errors=True)
    #     assert 400 == res.status_code
    #
    # def test_upload_file_with_expired_token(self, test_app, test_ip):
    #     delay = int(float(test_app.app.tokens[test_ip[1]]['Expiry']) - time.time() + 0.5)
    #     time.sleep(delay)
    #     res = test_app.post('/upload', {'token': test_ip[1]}, expect_errors=True)
    #     assert 403 == res.status_code
    #
    # def test_upload_file_with_wrong_token(self, test_app):
    #     res = test_app.post('/upload', {'token': ''}, expect_errors=True)
    #     assert 403 == res.status_code
    #     res = test_app.post('/upload', expect_errors=True)
    #     assert 403 == res.status_code
