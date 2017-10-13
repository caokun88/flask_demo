#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""


from flask import request

import service
from test_demo import test_app
from utils.respone_message import ok


@test_app.route('/')
def test_index_view():
    print request.host_url
    return ok(data={'platform': 'windows'.capitalize()})


@test_app.route('/add/role/')
def test_add_role_view():
    role = request.args.get('role')
    service.add_role(role)
    return 'ok'


@test_app.route('/modify/<int:role_id>/role/')
def test_modify_role_view(role_id):
    role = request.args.get('role')
    service.modify_role(role_id, role)
    return 'oks'
