# -*- coding: utf-8 -*-
from bottle import Bottle, request, response, HTTPResponse
from bottleship import BottleShip
import binascii
import os
import time


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


app = Bottle()
app.tokens = TokenManager(token_lifetime_seconds=5)


@app.route('/get_token')
def get_token():
    ip = request.query.ip
    if not ip:
        response.status = 400
        return 'IP parameter required'
    token = None
    for key, value in app.tokens.iteritems():
        if ip == value['IP']:
            token = key
            break
    if not token:
        token = app.tokens.add(ip)
    return {'Token': token}


def require_auth(path=None, method='GET', callback=None, name=None, apply_=None, skip=None, **config):
    def decorated(f):
        def route_do(**kwargs):
            callback_success = f or (lambda: HTTPResponse(status=200, body='OK'))
            if not app.tokens.check_token(request.query.token):
                response.status = 403
                return 'Auth error: Provided token does not exist or has expired.'
            return callback_success(**kwargs)

        return app.route(path, method, route_do, name, apply_, skip, **config)

    return decorated(callback) if callback else decorated


@require_auth('/import_file')
def import_file():
    pass


bs = BottleShip()
bs.route('/register', method=('GET', 'POST'), callback=bs.register)
bs.route('/login', method=('GET', 'POST'), callback=bs.login)


# This API endpoint can only be reached by users who have logged in
@bs.require_auth('/testapi', method=('GET', 'POST'))
def testapi(bottleship_user_record):
    return "Hello, %s!" % bottleship_user_record.get('Username')


@app.route('/')
def index():
    return 'Hi!'
