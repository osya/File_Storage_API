#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
import time
from bottle import Bottle, HTTPResponse, request, response


class TokenManager(dict):
    def __init__(self, token_lifetime_seconds=3600, *args, **kwargs):
        super(TokenManager, self).__init__(*args, **kwargs)
        self._token_lifetime_seconds = token_lifetime_seconds

    def add(self, ip):
        token = binascii.hexlify(os.urandom(8))
        # TODO: Check whether this token already exists
        self[token] = {
            'Expiry': str(time.time() + self._token_lifetime_seconds),
            'IP': ip
        }
        return token

    def check_token(self, token):
        return token and token in self and time.time() <= float(self[token].get('Expiry', '0'))


class IPAuth(Bottle):
    """ Bottle plugin for IP Authentication. Inspired by Bottleship """

    def __init__(self, token_manager=None, token_lifetime_seconds=3600):
        super(IPAuth, self).__init__()
        self._token_lifetime_seconds = token_lifetime_seconds
        self.tokens = token_manager or TokenManager(token_lifetime_seconds=self._token_lifetime_seconds)

    def require_auth(self, path=None, method='GET', callback=None, name=None, apply_=None, skip=None, **config):
        def decorated(f):
            def route_do(**kwargs):
                callback_success = f or (lambda: HTTPResponse(status=200, body='OK'))
                if not self.tokens.check_token(request.query.token):
                    response.status = 403
                    return 'Auth error: Provided token does not exist or has expired.'
                return callback_success(**kwargs)

            return self.route(path, method, route_do, name, apply_, skip, **config)

        return decorated(callback) if callback else decorated
