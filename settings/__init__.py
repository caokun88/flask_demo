#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

from flask import Flask
from index.views import index_app


app = Flask(__name__)

app.register_blueprint(index_app)
