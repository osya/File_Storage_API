# -*- coding: utf-8 -*-
from bottle import request, response, static_file
from file_storage.ipauth import IPAuth
import os
from file_storage import settings
import uuid
import zipfile
import glob
from StringIO import StringIO
from fdsend import send_file

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
    file_path = os.path.join(save_path, '%s_%s.zip' % (key, expired_date))
    zf = zipfile.ZipFile(file_path, mode='w')
    try:
        zf.writestr(f.filename, f.file.read())
    finally:
        zf.close()
    response.status = 200
    return {'Key': str(key)}


@app.require_auth('/download', method='GET')
def download():
    key = request.params.dict.get('Key')
    if key:
        key = key[0]
        if not key:
            response.status = 400
            return 'File Key is required'
    else:
        response.status = 400
        return 'File Key is required'

    for name in glob.glob(os.path.join(settings.STATIC_PATH, '%s_*.zip' % key)):
        zf = zipfile.ZipFile(name)
        unp = {name: zf.read(name) for name in zf.namelist()}.items()[0]
        return send_file(StringIO(unp[1]), filename=unp[0], attachment=True)

    response.status = 400
    return 'Wrong File Key'


@app.route('/')
def index():
    response.status = 200
    return
