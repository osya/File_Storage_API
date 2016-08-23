# -*- coding: utf-8 -*-
from bottle import request, response
from bottleship import BottleShip
from file_storage.ipauth import IPAuth

app = IPAuth(token_lifetime_seconds=3)


@app.route('/register')
def register():
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


@app.require_auth('/import_file')
def import_file():
    pass


@app.route('/')
def index():
    response.status = 200
    return
