# -*- coding: utf-8 -*-
from bottle import Bottle
from .controllers.home import app, bs


Routes = Bottle()
# App to render / (home)
Routes.merge(app)
Routes.merge(bs)
