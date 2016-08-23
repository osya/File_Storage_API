#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import click
from bottle import run
from file_storage import settings
from file_storage.app import create_app

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

app = create_app()


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
    return pytest.main([TEST_PATH, '--verbose'])


if __name__ == "__main__":
    # cmds()
    test()
