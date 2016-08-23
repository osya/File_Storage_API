# -*- coding: utf-8 -*-
from bottle import Bottle
from bottleship import BottleShip

home_app = Bottle()

bs = BottleShip()
bs.route('/register', method=('GET', 'POST'), callback=bs.register)
bs.route('/login', method=('GET', 'POST'), callback=bs.login)


# This API endpoint can only be reached by users who have logged in
@bs.require_auth('/testapi', method=('GET', 'POST'))
def testapi(bottleship_user_record):
    return "Hello, %s!" % bottleship_user_record.get('Username')


@home_app.route('/')
def index():
    return 'Hi!'
