#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

from flask_login import login_required

from index import index_app


@index_app.route('/index/', methods=['GET'])
@index_app.route('/', methods=['GET'])
@login_required
def index_view():
    return 'hello world！'
