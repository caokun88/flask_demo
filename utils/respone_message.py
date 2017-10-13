#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import json
from functools import partial

from flask import make_response


MESSAGE_DICT = {
    200: u'请求正常',

    400: u'请求参数错误',
    401: u'未授权（未登录）',
    403: u'没有访问权限',
    405: u'请求方式错误',

    500: u'内部服务器错误',
}


def __basic_response(code=None, data={}):
    message = MESSAGE_DICT.get(code)
    resp_data = {
        'code': code,
        'data': data,
        'msg': message
    }
    resp_data_str = json.dumps(resp_data, ensure_ascii=False)
    return make_response(resp_data_str)


ok = partial(__basic_response, code=200)
bad_request = partial(__basic_response, code=400)
no_auth = partial(__basic_response, code=401)
forbidden = partial(__basic_response, code=403)
request_method_error = partial(__basic_response, 405)
error = partial(__basic_response, 500)
