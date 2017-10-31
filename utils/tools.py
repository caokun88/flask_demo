#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import os
import uuid
import math
import datetime

import xlwt

from StringIO import StringIO
from flask import request, make_response
from settings import static_dir
from utils.constant import ALLOWED_EXTENSIONS

from utils.constant import DATE_TIME_FORMAT_2


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
    if not fee:
        fee = 0
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


def get_page(current_page, page_size, total_count):
    """
    获取分页的数据
    :param current_page: 当前页
    :param page_size: 也容量
    :param total_count: 总数量
    :return: page
    :rtype dict
    """
    total_page = int(math.ceil(total_count / float(page_size)))
    page = {
        'current_page': current_page, 'page_size': page_size, 'total_count': total_count, 'total_page': total_page
    }
    return page


def get_n_day_before(n_day):
    """
    获取几天前或者几天后的日期
    :param n_day: 天数
    :return:
    """
    now = datetime.datetime.now()
    n_datetime = now + datetime.timedelta(days=n_day)
    return n_datetime


def download_excel(header_list, content_list):
    """
    导出excel
    :param header_list: 头list
    :param content_list: content list 二维数组
    :return:
    """
    wb = xlwt.Workbook(encoding='utf8')
    ws = wb.add_sheet('rfr')
    for i, header in enumerate(header_list):
        ws.write(0, i, header)
    for j, contents in enumerate(content_list, start=1):
        for n, content in enumerate(contents):
            ws.write(j, n, content)
    buf = StringIO()
    wb.save(buf)
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = "application/vnd.ms-excel"
    response.headers['Content-Disposition'] = 'attachment; filename=订单{}.xls'.format(
        datetime.datetime.now().strftime(DATE_TIME_FORMAT_2)
    )
    return response
