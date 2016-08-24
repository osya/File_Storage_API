# -*- coding: utf-8 -*-
from bottle import request, response
from file_storage.ipauth import IPAuth
import os
from file_storage import settings
import uuid

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
    expired_date = request.params.dict.get('expired_date')
    if expired_date:
        expired_date = expired_date[0]
        if not expired_date:
            response.status = 400
            return 'expired_date is required'
    else:
        response.status = 400
        return 'expired_date is required'

    key = uuid.uuid4()
    save_path = settings.STATIC_PATH
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    name, ext = f.filename.split('.')
    file_path = os.path.join(save_path, '%s_%s.%s' % (key, expired_date, ext))
    f.save(file_path, overwrite=True)
    response.status = 200
    return {'Key': str(key)}


@app.route('/')
def index():
    response.status = 200
    return
