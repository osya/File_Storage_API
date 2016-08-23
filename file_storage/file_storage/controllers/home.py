# -*- coding: utf-8 -*-
from bottle import Bottle, request, response
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


app = Bottle()
app.tokens = TokenManager(token_lifetime_seconds=1)


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


@app.route('/import_file')
def import_file():
    token = request.query.token
    if not token or token not in app.tokens or time.time() > float(app.tokens[token].get('Expiry', '0')):
        response.status = 403
        return 'Auth error: Provided token does not exist or has expired.'


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
