# -*- coding: utf-8 -*-
import datetime as dt
import glob
import os
import uuid
import zipfile
from StringIO import StringIO
from bottle import request, HTTPError
from bottle_sqlite import SQLitePlugin
from fdsend import send_file
from file_storage import settings
from file_storage.ipauth import IPAuth

app = IPAuth(token_lifetime_seconds=5)
app.install(SQLitePlugin(dbfile=os.path.abspath(os.path.join(settings.PROJECT_PATH, '..', settings.SQLITE_FILE_NAME))))


@app.route('/register')
def register():
    ip = request.query.ip
    if not ip:
        return HTTPError(400, 'IP parameter required')
    token = None
    for key, value in app.tokens.iteritems():
        if ip == value['IP']:
            token = key
            break
    if not token:
        token = app.tokens.add(ip)
    return {'Token': token}


@app.require_auth('/upload', method='POST')
def upload(db):
    f = request.files.get('upload')
    expired_date = request.params.dict.get('expired_date')
    if expired_date:
        expired_date = expired_date[0]
        if not expired_date:
            return HTTPError(400, 'expired_date is required')
    else:
        return HTTPError(400, 'expired_date is required')

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

    db.execute('INSERT INTO access_log (file_key) VALUES (?)', (str(key), ))
    return {'Key': str(key)}


@app.require_auth('/download', method='GET')
def download(db):
    key = request.params.dict.get('Key')
    if key:
        key = key[0]
        if not key:
            return HTTPError(400, 'File Key is required')
    else:
        return HTTPError(400, 'File Key is required')

    for name in glob.glob(os.path.join(settings.STATIC_PATH, '%s_*.zip' % key)):
        zf = zipfile.ZipFile(name)
        unp = {name: zf.read(name) for name in zf.namelist()}.items()[0]
        return send_file(StringIO(unp[1]), filename=unp[0], attachment=True)

    db.execute('UPDATE access_log SET access_date = ? WHERE file_key = ?', (dt.datetime.utcnow(), str(key)))

    return HTTPError(400, 'Wrong File Key')


@app.route('/')
def index():
    return ''
