#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

from flask import Blueprint

order_app = Blueprint('order', __name__, static_folder='../templates')
