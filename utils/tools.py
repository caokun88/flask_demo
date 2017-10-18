#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import os
import uuid

from flask import request
from settings import static_dir
from utils.constant import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    上传文件是否合适
    :param filename: 文件名称
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file_obj, path_dir):
    """
    上传图片
    :param file_obj: 文件对象
    :param path_dir 路径
    :return:
    """
    if file_obj and allowed_file(file_obj.filename):
        ext = file_obj.filename.split(u'.')[-1]
        filename = u'{}.{}'.format(uuid.uuid4().hex, ext)
        file_obj.save(os.path.join(static_dir, path_dir, filename))
        return u'{}/{}/{}'.format('static', path_dir, filename)


def format_fee(fee):
    """
    格式化金额
    :param fee: 金额 （分）
    :return: fee （元）
    """
    fee_float = round(fee / 100.0, 2)
    fee = int(fee_float) if fee_float == int(fee_float) else fee_float
    return fee


def is_ajax():
    """
    判断请求是否为ajax
    :return:
    """
    ajax = request.headers.get('X-Requested-With')
    if ajax == 'XMLHttpRequest':
        return True
    return False
