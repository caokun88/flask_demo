#!/usr/bin/env python
# coding=utf8

"""
@author: caokun
"""

from settings import model_test, app


@model_test.connect_via(sender=app)
def test_send(sender, obj, **extra):
    print sender
    print type(sender)
    print obj
    print type(obj)
    print extra
    print obj.role
    print u'我是信号{}'.format(model_test.name)