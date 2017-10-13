#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

import platform
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config


system = platform.system()
if system == 'Windows':
    env = 'dev'
else:
    env = 'deploy'
app = Flask(__name__, template_folder='../templates/')
app.config.from_object(config[env])
db = SQLAlchemy(app)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_dir = os.path.join(base_dir, 'static')

