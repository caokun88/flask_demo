#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from model import db, PayProject


def get_project_list():
    """
    获取商品列表
    :return:
    """
    project_obj_list = PayProject.query.all().order_by(db.desc(PayProject.order_index))
    project_list = list()
    for project_obj in project_obj_list:
        project_list.append({
            'id': project_obj.id,
            'name': project_obj.name,
            'agent_fee': project_obj.agent_fee,
            'selling_fee': project_obj.selling_fee,
            'icon': project_obj.icon,
            'order_index': PayProject.order_index
        })
    return project_list
