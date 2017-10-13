#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

import platform

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config


system = platform.system()
if system == 'Windows':
    env = 'dev'
else:
    env = 'deploy'
app = Flask(__name__)
app.config.from_object(config[env])
db = SQLAlchemy(app)
