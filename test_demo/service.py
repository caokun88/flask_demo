#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from model import db, TestRole


def add_role(role):
    role_obj = TestRole(role=role)
    db.session.add(role_obj)
    db.session.commit()


def modify_role(role_id, role):
    print role_id
    role_obj = TestRole.query.filter_by(id=role_id).first()
    print role_obj
    if role_obj:
        print 'user'
        role_obj.role = role
        db.session.commit()
        print '23'
