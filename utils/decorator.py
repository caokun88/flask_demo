#! /usr/bin/env python
# coding=utf8
# create by caokun on 2017-08-21

import time
from functools import wraps

from flask import g, request, redirect, url_for
from respone_message import request_method_error, no_auth, forbidden
import tools


def require_method(methods):
    """
    请求方式过滤
    :param methods: list, ['POST']
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if request.method.upper() in methods:
                return func(*args, **kwargs)
            return request_method_error()
        return inner
    return wrapper


def require_permission(func):
    """
    权限过滤过滤
    :param func:
    :return:
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user.role_obj.role == 'super':
            return func(*args, **kwargs)
        is_ajax = tools.is_ajax()
        if is_ajax:
            return forbidden()
        else:
            return redirect(url_for('index.forbidden_view'))
    return inner


def used_time(func):
    """
    运行时间装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print 'this func used time is == {}'.format(end_time - start_time)
        return f
    return inner
