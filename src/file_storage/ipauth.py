#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from functools import wraps
from inspect import formatargspec, getargspec

from bottle import Bottle, HTTPResponse, request, response


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


class IPAuth(Bottle):
    """ Bottle plugin for IP Authentication. Inspired by Bottleship """

    def __init__(self, token_manager=None, token_lifetime_seconds=3600):
        super(IPAuth, self).__init__()
        self._token_lifetime_seconds = token_lifetime_seconds
        self.tokens = token_manager or TokenManager(token_lifetime_seconds=self._token_lifetime_seconds)

    def require_auth(self, path=None, method='GET', callback=None, name=None, apply_=None, skip=None, **config):
        # Inspired by https://emptysqua.re/blog/copying-a-python-functions-signature/
        def decorated(f):
            def route_do(*args, **kwargs):
                callback_success = f or (lambda: HTTPResponse(status=200, body='OK'))
                token = request.params.dict.get('token')
                if not token or not self.tokens.check_token(token[0]):
                    response.status = 403
                    return 'Auth error: Provided token does not exist or has expired.'
                return callback_success(*args, **kwargs)

            formatted_args = formatargspec(*getargspec(f))
            fn_def = 'lambda %s: route_do%s' % (formatted_args.lstrip('(').rstrip(')'), formatted_args)
            return self.route(path, method, wraps(f)(eval(fn_def, {'route_do': route_do})), name, apply_, skip,
                              **config)

        return decorated(callback) if callback else decorated
