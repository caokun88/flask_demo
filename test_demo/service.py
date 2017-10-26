#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from model import db, TestRole, TestUser
from settings import model_test, app


def add_role(role):
    role_obj = TestRole(role=role)
    db.session.add(role_obj)
    db.session.commit()
    model_test.send(app, obj=role_obj)


def modify_role(role_id, role):
    role_obj = TestRole.query.filter_by(id=role_id).first()
    if role_obj:
        role_obj.role = role
        db.session.commit()


def back_ref_test():
    user_obj = TestUser.query.filter_by(id=1).first()
    # print user_obj.testuser_set
    print user_obj.role

    role_obj = TestRole.query.filter_by(id=2).first()
    print str(role_obj.testuser_set)

    user_obj_list = TestUser.query.join(TestRole).filter_by(role='sup4').all()
    for obj in user_obj_list:
        print obj.name
    print str(TestUser.query.join(TestRole).filter_by(role='sup4'))