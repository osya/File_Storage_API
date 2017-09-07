#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from functools import wraps

from bottle import HTTPError, request


class TokenManager(dict):
    def __init__(self, token_lifetime_seconds=3600, *args, **kwargs):
        super(TokenManager, self).__init__(*args, **kwargs)
        self._token_lifetime_seconds = token_lifetime_seconds

    def add(self, ip):
        token = os.urandom(8).hex()
        # TODO: Check whether this token already exists
        self[token] = {
            'Expiry': str(time.time() + self._token_lifetime_seconds),
            'IP': ip
        }
        return token

    def check_token(self, token):
        return token and token in self and time.time() <= float(self[token].get('Expiry', '0'))


class IPAuthPlugin(object):
    """ Bottle plugin for IP Authentication. Inspired by Bottleship """

    keyword = 'auth'

    def __init__(self, token_manager=None, token_lifetime_seconds=3600):
        super(IPAuthPlugin, self).__init__()
        self._token_lifetime_seconds = token_lifetime_seconds
        self.tokens = token_manager or TokenManager(token_lifetime_seconds=self._token_lifetime_seconds)

    def setup(self, app):
        app.tokens = self.tokens

    def apply(self, callback, route):
        auth_value = route.get('config').get(self.keyword, None)
        if not auth_value:
            return callback

        @wraps(callback)
        def wrapper(*args, **kwargs):
            token = request.params.dict.get('token')
            if not token:
                raise HTTPError(403, 'Auth error: Token required')
            if self.tokens.check_token(token[0]):
                return callback(*args, **kwargs)
            else:
                raise HTTPError(401, 'Auth error: Provided token does not exist or has expired')
        return wrapper


Plugin = IPAuthPlugin
