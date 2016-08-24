#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import click
from bottle import run
from file_storage import settings
from file_storage.controllers.api import app
from multiprocessing import Process
import time
import datetime as dt


@click.group()
def cmds():
    pass


@cmds.command()
@click.option('--port', default=os.environ.get('PORT', 8080), type=int,
              help=u'Set application server port!')
@click.option('--ip', default='127.0.0.1', type=str,
              help=u'Set application server ip!')
@click.option('--debug', default=False,
              help=u'Set application server debug!')
def runserver(port, ip, debug):
    click.echo('Start server at: {}:{}'.format(ip, port))
    run(app=app, host=ip, port=port, debug=debug, reloader=debug)


# @cmds.command()
def test():
    import pytest
    return pytest.main([settings.TEST_PATH, '--verbose'])


def file_removal(path):
    # TODO: When deleting file delete corresponding record from SQLite database
    while 1:
        cur_date = dt.datetime.utcnow().date()
        for dirpath, _, filenames in os.walk(path):
            for file_name in filenames:
                exp_date = dt.datetime.strptime(file_name.split('.')[0].split('_')[1], '%Y-%m-%d').date()
                if cur_date > exp_date:
                    file_path = os.path.join(dirpath, file_name)
                    os.remove(file_path)

        time.sleep(60)


if __name__ == "__main__":
    frp = Process(target=file_removal, args=(settings.STATIC_PATH,))
    frp.start()

    import bottle
    bottle.debug(mode=True)

    # cmds()
    test()
