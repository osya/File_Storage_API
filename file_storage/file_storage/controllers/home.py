# -*- coding: utf-8 -*-
from bottle import Bottle, request
from bottleship import BottleShip
import binascii
import os

app = Bottle()
app.tokens = {}


@app.route('/get_token')
def get_token():
    ip = request.query.ip
    if ip in app.tokens:
        return app.tokens[ip]
    else:
        token = binascii.hexlify(os.urandom(8))
        app.tokens[ip] = token
        return {'Token': token}


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
