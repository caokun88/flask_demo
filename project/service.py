#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from model import db, PayProject
from utils import tools


def get_project(host_url, project_id):
    if project_id:
        project_obj = PayProject.query.filter_by(id=project_id).first()
        if not project_obj:
            return 3
        temp_data = {
            'id': project_obj.id,
            'name': project_obj.name,
            'agent_fee': project_obj.agent_fee,
            'selling_fee': project_obj.selling_fee,
            'icon': u'{}{}'.format(host_url, project_obj.icon) if project_obj.icon else '',
            'order_index': project_obj.order_index
        }
    else:
        temp_data = {}
    return temp_data


def get_project_list(host_url):
    """
    获取商品列表
    :param host_url: 域名
    :return:
    """
    project_obj_list = PayProject.query.order_by(db.desc(PayProject.order_index)).all()
    project_list = list()
    for project_obj in project_obj_list:
        project_list.append({
            'id': project_obj.id,
            'name': project_obj.name,
            'agent_fee': tools.format_fee(project_obj.agent_fee),
            'selling_fee': tools.format_fee(project_obj.selling_fee),
            'icon': u'{}{}'.format(host_url, project_obj.icon) if project_obj.icon else '',
            'order_index': project_obj.order_index
        })
    return project_list


def add_or_modify_project(name, agent_fee, selling_fee, icon, order_index, project_id=None):
    if project_id:
        # modify
        project_obj = PayProject.query.filter_by(id=project_id).first()
        if not project_obj:
            return 3
    else:
        project_obj = PayProject()
    try:
        project_obj.name = name
        project_obj.agent_fee = agent_fee
        project_obj.selling_fee = selling_fee
        project_obj.icon = icon
        project_obj.order_index = order_index
        db.session.add(project_obj)
        db.session.commit()
        msg = 1
    except Exception as e:
        print e
        msg = 2
        db.session.rollback()
    return msg
