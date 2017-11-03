#!/usr/bin/env python
# coding=utf8

"""
create on 2017-11-01
@author: cao kun
二维码
"""

import os

import qrcode

from PIL import Image
from settings import base_dir


def general_simple_qrcode(data='http://kunrui.xin/'):
    """
    生成简单的qrcode
    :param data: 连接
    :return:
    """
    qr_img = qrcode.make(data=data)
    return qr_img


def general_qrcode(data='http://kunrui.xin/', is_use_icon=False):
    """
    自定义参数的qrcode，也可以在二维码中增加logo
    :param data: url
    :param is_use_icon: 是否使用logo
    :return:
    """
    qr = qrcode.QRCode(
        version=10,  # (1, 40)
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,  # default 10
        border=1,  # default 4
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image()
    if is_use_icon is False:
        return qr_img

    qr_img = qr_img.convert('RGBA')
    icon = Image.open(os.path.join(base_dir, 'static/favicon.ico'))

    factor = 4
    qr_img_w, qr_img_h = qr_img.size

    size_w = int(qr_img_w / factor)
    size_h = int(qr_img_h / factor)

    icon_w, icon_h = icon.size

    icon_w = icon_w if icon_w < size_w else size_w
    icon_h = icon_h if icon_h < size_h else size_h

    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((qr_img_w - icon_w) / 2)
    h = int((qr_img_h - icon_h) / 2)
    qr_img.paste(icon, (w, h))
    return qr_img
