#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import datetime

from settings import db


class PayProject(db.Model):
    __bind_key__ = 'flask_demo'
    __tablename__ = 'pay_project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    all_agent_fee = db.Column(db.Integer, default=0)
    normal_agent_fee = db.Column(db.Integer, default=0)
    selling_fee = db.Column(db.Integer)
    icon = db.Column(db.String(255))
    order_index = db.Column(db.SmallInteger, index=True)  # 排序
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)
