#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""


from flask import request, make_response

import service
from test_demo import test_app
from utils.respone_message import ok
from tasks.test import test_celery
from utils import qr_code
from cStringIO import StringIO
from settings import cache


@test_app.route('/')
def test_index_view():
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


@test_app.route('/backref/')
def test_backref_view():
    service.back_ref_test()
    return 'oks'


@test_app.route('/celery/')
def celery_test_view():
    x = request.args.get('x', '13')
    y = request.args.get('y', '14')
    test_celery.delay(x, y)
    return ok()


@test_app.route('/qrcode/')
def qrcode_test_view():
    qr_img = qr_code.general_qrcode(is_use_icon=True)
    buf = StringIO()
    qr_img.save(buf, 'png')
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@test_app.route('/test-cache1/')
@cache.cached(timeout=30, key_prefix='test-cache1')
def test_cache1():
    print 'test_cache1'
    return 'test_cache1 success'


@test_app.route('/test-cache2/')
def test_cache2():
    l = ['caokun', 'renfurui']
    cache.set('l', l, 60 * 1)
    print 'set success'
    return 'success set'


@test_app.route('/test-cache3/')
def test_cache3():
    l = cache.get('l')
    print l
    print 'get success'
    return str(l)