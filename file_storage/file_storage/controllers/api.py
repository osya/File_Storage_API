# -*- coding: utf-8 -*-
from bottle import request, response
from file_storage.ipauth import IPAuth
import os
from file_storage import settings

app = IPAuth(token_lifetime_seconds=5)


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


@app.require_auth('/upload', method='POST')
def upload():
    f = request.files.get('upload')
    save_path = settings.STATIC_PATH
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = os.path.join(save_path, f.filename)
    f.save(file_path, overwrite=True)
    response.status = 200
    return "File successfully saved to '{0}'.".format(save_path)


@app.route('/')
def index():
    response.status = 200
    return
