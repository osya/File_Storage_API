#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt
import os
import time
from glob import glob
from multiprocessing import Process
from subprocess import call

import click
from bottle_sqlite import SQLitePlugin

from bottle import run
from file_storage import settings
from file_storage.bottle_ipauth import IPAuthPlugin
from file_storage.controllers.api import api


@click.group()
def cmds():
    pass


@cmds.command()
@click.option('--port', default=os.environ.get('PORT', 8080), type=int, help='Set application server port!')
@click.option('--ip', default='127.0.0.1', type=str, help='Set application server ip!')
@click.option('--debug', default=False, help='Set application server debug!')
def runserver(port, ip, debug):
    frp = Process(target=file_removal, args=(settings.STATIC_PATH,))
    frp.start()
    # TODO: Investigate ResourceWarning: unclosed <socket.socket fd=860, family=AddressFamily.AF_INET,
    # type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 11652), raddr=('127.0.0.1', 11642)>
    click.echo('Start server at: {}:{}'.format(ip, port))
    api.install(
        SQLitePlugin(dbfile=os.path.abspath(os.path.join(settings.PROJECT_PATH, '..', settings.SQLITE_FILE_NAME))))
    api.install(IPAuthPlugin())
    run(app=api, host=ip, port=port, debug=debug, reloader=debug)


@cmds.command()
def test():
    import pytest
    return pytest.main([settings.TEST_PATH, '--verbose'])


@cmds.command()
@click.option('-f', '--fix-imports', is_flag=True, default=False, help='Fix imports using isort, before linting')
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""

    skip = ['requirements', 'env']
    root_files = glob('*.py')
    root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        print('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv is not 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


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


if __name__ == '__main__':
    cmds()

# TODO: Currently SQLite database used in dev & prod. Change database for prod
