#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

from flask import render_template
from flask_login import login_required

from utils import decorator
from index import index_app


@index_app.route('/index/', methods=['GET'])
@index_app.route('/', methods=['GET'])
@login_required
def index_view():
    return render_template('base/base.html')


@index_app.route('/forbidden/', methods=['GET'])
def forbidden_view():
    return render_template('error/403.html')
