# -*- coding: utf-8 -*-
from bottle import Bottle, request, response
from bottleship import BottleShip
import binascii
import os

app = Bottle()
app.tokens = {}


@app.route('/get_token')
def get_token():
    ip = request.query.ip
    if not ip:
        response.status = 400
        return 'IP parameter required'
    if ip not in app.tokens:
        app.tokens[ip] = binascii.hexlify(os.urandom(8))
    return {'Token': app.tokens[ip]}


@app.route('/import_file')
def import_file():
    token = request.query.token
    if not token or token not in app.tokens.values():
        response.status = 401
        return 'Wrong token'
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
