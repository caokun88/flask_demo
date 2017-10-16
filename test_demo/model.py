#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import datetime

from settings import db


class TestUser(db.Model):
    __bind_key__ = 'flask_demo'
    __tablename__ = 'test_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('test_role.id'))
    role = db.relationship('TestRole', backref=db.backref('testuser_set'))
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    up_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)


class TestRole(db.Model):
    __bind_key__ = 'flask_demo'
    __tablename__ = 'test_role'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), default='super')
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)

