#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

from flask import Blueprint
from flask_login import LoginManager
from settings import app

import signal

auth_app = Blueprint('auth', __name__, template_folder='../templates/')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login_view'

