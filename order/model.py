#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import datetime

from settings import db


class PayOrder(db.Model):
    __bind_key__ = 'flask_demo'
    __tablename__ = 'pay_order'

    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, db.ForeignKey('project.pay_project.id'))
    real_fee = db.Column(db.Integer)  # 实际支付金额（分）
    name = db.Column(db.String(64))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    pay_type = db.Column(db.String(20))  # 微信or支付宝（wechat_pay or ali_pay）
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    update_time = db.Column(db.TIMESTAMP, onupdate=datetime.datetime.now)
