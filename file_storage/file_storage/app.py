#!/usr/bin/env python
# -*- coding: utf-8 -*-
from file_storage.controllers.api import app as api


def create_app():
    return api
