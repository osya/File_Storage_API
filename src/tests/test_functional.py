#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt
import os
import re

from file_storage import settings


# noinspection PyClassHasNoInit
# It is one class for all tests because it is needed to use single instance of Bottle app
class TestFunctional:
    def test_upload_file_with_correct_token(self, test_app):
        with open(os.path.join(os.path.dirname(os.path.dirname(settings.TEST_PATH)), 'README.md'), 'rb') as f:
            res = test_app.post(
                '/upload',
                {
                    'token': test_app.token,
                    'expired_date': dt.datetime.utcnow().date()
                },
                upload_files=[('upload', 'README.md', f.read())])
            assert 200 == res.status_code

    def test_download_file_with_correct_token(self, test_app, file_key):
        res = test_app.get('/download', {'token': test_app.token, 'Key': file_key})
        assert 200 == res.status_code
        assert res.body

        filename = None
        for header in res.headerlist:
            if type(header) is tuple:
                for item in header:
                    m = re.search(r'^.*filename="(.*)"$', item)
                    if m:
                        filename = m.group(1)
                        break
            if filename:
                break

        assert filename

    def test_download_file_with_wrong_key(self, test_app):
        res = test_app.get('/download', {'token': test_app.token, 'Key': ''}, expect_errors=True)
        assert 400 == res.status_code
        res = test_app.get('/download', {'token': test_app.token}, expect_errors=True)
        assert 400 == res.status_code

    def test_upload_file_with_wrong_expired_date(self, test_app):
        res = test_app.post('/upload', {'token': test_app.token, 'expired_date': ''}, expect_errors=True)
        assert 400 == res.status_code
        res = test_app.post('/upload', {'token': test_app.token}, expect_errors=True)
        assert 400 == res.status_code

    # def test_upload_file_with_expired_token(self, test_app):
    #     import time
    #     delay = int(float(test_app.app.tokens[test_app.token]['Expiry']) - time.time() + 0.5)
    #     time.sleep(delay)
    #     res = test_app.post('/upload', {'token': test_app.token}, expect_errors=True)
    #     assert 401 == res.status_code

    def test_upload_file_with_wrong_token(self, test_app):
        res = test_app.post('/upload', {'token': ''}, expect_errors=True)
        assert 401 == res.status_code
        res = test_app.post('/upload', expect_errors=True)
        assert 403 == res.status_code
