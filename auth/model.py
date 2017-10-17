#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from settings import db


class User(UserMixin, db.Model):

    __bind_key__ = 'flask_demo'
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(64))
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    wechat = db.Column(db.String(64))
    role_id = db.Column(db.ForeignKey('role.id'))
    role_obj = db.relationship('Role', backref=db.backref('user_set'))
    c_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    up_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')
    #
    # @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Role(db.Model):

    __bind_key__ = 'flask_demo'
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), nullable=False, server_default='user')
    level = db.Column(db.String(32), default='', nullable=False)
    c_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    up_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)
