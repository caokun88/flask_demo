#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import datetime

from settings import db
from project.model import PayProject


class PayOrder(db.Model):
    __bind_key__ = 'flask_demo'
    __tablename__ = 'pay_order'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('pay_project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    real_fee = db.Column(db.Integer)  # 实际支付金额（分）
    name = db.Column(db.String(64))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    pay_type = db.Column(db.String(20))  # 微信or支付宝（wechat_pay or ali_pay）
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)
    project_obj = db.relationship('PayProject', backref=db.backref('payproject_set'))
    user_obj = db.relationship('User', backref=db.backref('user_set'))
    deleted = db.Column(db.Boolean, default=False, nullable=False)  # 是否显示
