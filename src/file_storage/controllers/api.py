# -*- coding: utf-8 -*-
import datetime as dt
import glob
import os
import uuid
import zipfile
from io import BytesIO

from fdsend import send_file

from bottle import Bottle, HTTPError, request
from file_storage import settings

api = Bottle()


@api.route('/register')
def register():
    ip = request.remote_addr
    token = None
    for key, value in api.tokens.items():
        if ip == value['IP']:
            token = key
            break
    if not token:
        token = api.tokens.add(ip)
    return {'Token': token}


@api.post('/upload', auth='ipauth')
def upload(db):
    f = request.files.get('upload')
    expired_date = request.params.dict.get('expired_date')
    if expired_date:
        expired_date = expired_date[0]
        if not expired_date:
            return HTTPError(400, 'expired_date is required')
    else:
        return HTTPError(400, 'expired_date is required')

    save_path = os.path.join(
        settings.STATIC_PATH,
        request.params.dict.get('token')[0],
        str(dt.datetime.utcnow().date()))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    key = uuid.uuid4()
    file_path = os.path.join(save_path, '%s_%s.zip' % (key, expired_date))
    zf = zipfile.ZipFile(file_path, mode='w')
    try:
        zf.writestr(f.filename, f.file.read())
    finally:
        zf.close()

    return {'Key': str(key)}


@api.get('/download', auth='ipauth')
def download(db):
    key = request.params.dict.get('Key')
    if key:
        key = key[0]
        if not key:
            return HTTPError(400, 'File Key is required')
    else:
        return HTTPError(400, 'File Key is required')

    for name in glob.glob(os.path.join(
        settings.STATIC_PATH,
        request.params.dict.get('token')[0],
        '*',
            '%s_*.zip' % key)):
        zf = zipfile.ZipFile(name)
        unp = list({name: zf.read(name) for name in zf.namelist()}.items())[0]
        cur_date = dt.datetime.utcnow()
        db.execute('INSERT INTO access_log (file_key, access_date) VALUES (?, ?)', (key, cur_date))
        db.execute('UPDATE access_log SET last_access_date =\n'
                   '(SELECT MAX(access_date) FROM access_log WHERE file_key = ?)\n'
                   'WHERE file_key = ?', (key, key))
        # TODO: Use SQLAlchemy instead of raw SQL queries
        return send_file(BytesIO(unp[1]), filename=unp[0], attachment=True)

    return HTTPError(400, 'Wrong File Key')


@api.route('/')
def index():
    return ''
