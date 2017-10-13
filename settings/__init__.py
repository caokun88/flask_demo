#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config


env = os.getenv('app_env', 'dev')
app = Flask(__name__)
app.config.from_object(config[env])
db = SQLAlchemy(app)
