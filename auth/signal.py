#!/usr/bin/env python
# coding=utf8

"""
@author: caokun
"""

import datetime

from flask import request
from flask_login import user_logged_in
from settings import app
from model import db


@user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    login_count = user.login_count if user.login_count else 0
    user.login_count = login_count + 1
    user.login_last_ip = request.remote_addr
    user.login_last_time = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
