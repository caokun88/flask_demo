#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""


class BaseConfig(object):  # 基本配置类
    SECRET_KEY = 'asdasdfadsfadsfadfafdsa'
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 2
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    ITEMS_PER_PAGE = 10


class DevConfig(BaseConfig):
    SQLALCHEMY_BINDS = {
        'flask_demo': 'mysql+pymysql://root@127.0.0.1/flask_demo?charset=utf8mb4'
    }
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_BINDS['flask_demo']


class DeployConfig(BaseConfig):
    DEBUG = False
    PERMANENT_SESSION_LIFETIME = 60 * 60
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kunrui1314@127.0.0.1/flask_demo?charset=utf8mb4'
    SQLALCHEMY_BINDS = {
        'flask_demo': 'mysql+pymysql://root:kunrui1314@127.0.0.1/flask_demo?charset=utf8mb4'
    }
    # WTF_CSRF_ENABLED = False


config = {
    'dev': DevConfig,
    'deploy': DeployConfig
}