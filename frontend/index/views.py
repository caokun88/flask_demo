#!/usr/bin/env python
# coding=utf8

"""
create on 2018-01-18
@author: cao kun
"""

from flask import render_template, redirect, url_for
from flask_login import login_required

from utils import decorator
from frontend import frontend_app


@frontend_app.route('/index/', methods=['GET'])
@frontend_app.route('/', methods=['GET'])
def index_view():
    return redirect(url_for('index.index_view'))
