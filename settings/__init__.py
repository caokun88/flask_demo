#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

import platform
import os
import redis

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect  # CsrfProtect
from blinker import Namespace

from config import config


system = platform.system()
if system == 'Windows':
    env = 'dev'
else:
    env = 'deploy'
app = Flask(__name__, template_folder='../templates/')
app.config.from_object(config[env])
db = SQLAlchemy(app)
csrf = CSRFProtect()
csrf.init_app(app)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_dir = os.path.join(base_dir, 'static')

test_signals = Namespace()
model_test = test_signals.signal('model_test')

# redis
pool = redis.ConnectionPool(
    host='127.0.0.1',
    port=6379,
    db=0,
    password=None
)

redis_conn = redis.StrictRedis(connection_pool=pool)
