#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

import operator

from flask import g

from model import db, PayOrder
from project.model import PayProject
from utils import tools
from utils.constant import DATE_TIME_FORMAT


def add_order_model(order_id, project_id, real_fee, name, address, phone, pay_type, user):
    if order_id:
        order_obj = PayOrder.query.filter(PayOrder.id == order_id, PayOrder.user_id == user.id).first()
    else:
        order_obj = PayOrder(user_id=user.id)
    order_obj.project_id = project_id,
    order_obj.real_fee = real_fee,
    order_obj.name = name,
    order_obj.address = address,
    order_obj.phone = phone,
    order_obj.pay_type = pay_type
    db.session.add(order_obj)
    db.session.commit()


def get_order_list_model(start_time, end_time, project_id, keyword, user, current_page, page_size, deleted=0, label='select'):
    order_obj_list = PayOrder.query.filter(PayOrder.deleted == deleted, PayOrder.user_id == user.id)
    if start_time:
        order_obj_list = order_obj_list.filter(
            PayOrder.create_time >= start_time
        )
    if end_time:
        order_obj_list = order_obj_list.filter(
            PayOrder.create_time <= end_time
        )
    if project_id:
        order_obj_list = order_obj_list.filter(PayOrder.project_id == project_id)
    if keyword:
        order_obj_list = order_obj_list.filter(PayOrder.phone == keyword)
    total_count = order_obj_list.count()
    order_obj_list = order_obj_list.order_by(db.desc(PayOrder.id))
    if label == 'select':
        order_obj_list = order_obj_list.offset((current_page - 1) * page_size).limit(page_size)
        page = tools.get_page(current_page, page_size, total_count)
        return order_obj_list, page
    else:
        return order_obj_list


def order_statistics(start_time, end_time, project_id, keyword, user, deleted=0):
    """
    订单统计
    :param start_time:
    :param end_time:
    :param project_id:
    :param keyword:
    :param user:
    :param deleted:
    :return: (real_fee, normal_agent_fee, all_agent_fee)
    """
    order_obj_list = db.session.query(
        db.func.sum(PayOrder.real_fee), db.func.sum(PayProject.normal_agent_fee), db.func.sum(PayProject.all_agent_fee)
    ).join(PayProject, PayOrder.project_id==PayProject.id).filter(
        PayOrder.deleted == deleted, PayOrder.user_id == user.id
    )
    if start_time:
        order_obj_list = order_obj_list.filter(
            PayOrder.create_time >= start_time
        )
    if end_time:
        order_obj_list = order_obj_list.filter(
            PayOrder.create_time <= end_time
        )
    if project_id:
        order_obj_list = order_obj_list.filter(PayOrder.project_id == project_id)
    if keyword:
        order_obj_list = order_obj_list.filter(PayOrder.phone == keyword)

    return order_obj_list.first()


def delete_order_model(order_id, user):
    """
    删除订单
    :param order_id:
    :param user:
    :return:
    """
    order_obj_list = PayOrder.query.filter(PayOrder.id == order_id, PayOrder.user_id == user.id)
    order_obj_list.update({'deleted': 1})
    db.session.commit()

"""
service
"""


def get_order_list_service(start_time, end_time, project_id, keyword, user, current_page, page_size, deleted=0, label='select'):
    order_obj_list, page = get_order_list_model(start_time, end_time, project_id, keyword, user, current_page, page_size, deleted=deleted, label=label)
    order_list = list()
    total_flowing_fee = 0  # 流水
    total_profit_fee = 0  # 利润
    for order_obj in order_obj_list:
        project_obj = order_obj.project_obj
        agent_fee = tools.format_fee(project_obj.all_agent_fee) if g.user.level == 'all' else tools.format_fee(project_obj.normal_agent_fee)
        profit_fee = tools.format_fee(order_obj.real_fee) - agent_fee
        selling_fee = tools.format_fee(project_obj.selling_fee)
        _real_fee = tools.format_fee(order_obj.real_fee)
        order_list.append({
            'id': order_obj.id,
            'project_id': project_obj.id,
            'project_name': project_obj.name,
            'agent_fee': agent_fee,
            'selling_fee': selling_fee,
            'real_fee': _real_fee,
            'profit_fee': profit_fee,
            'pay_type': u'微信' if order_obj.pay_type == 'wechat_pay' else u'支付宝',
            'name': order_obj.name,
            'address': order_obj.address,
            'phone': order_obj.phone,
            'create_time': order_obj.create_time.strftime(DATE_TIME_FORMAT)
        })
        total_flowing_fee += _real_fee
        total_profit_fee += profit_fee
    return order_list, page, total_flowing_fee, total_profit_fee


def get_order_info(order_id):
    order_info = dict()
    order_obj = PayOrder.query.filter(PayOrder.id == order_id).first()
    if order_obj:
        project_obj = order_obj.project_obj
        order_info = {
            'id': order_obj.id,
            'project_id': project_obj.id,
            'project_name': project_obj.name,
            'real_fee': order_obj.real_fee,
            'pay_type': u'微信' if order_obj.pay_type == 'wechat_pay' else u'支付宝',
            'name': order_obj.name,
            'address': order_obj.address,
            'phone': order_obj.phone,
            'create_time': order_obj.create_time.strftime(DATE_TIME_FORMAT)
        }
    return order_info


def order_statics_service(start_time, end_time, project_id, keyword, user, deleted=0):
    real_fee, normal_agent_fee, all_agent_fee = order_statistics(
        start_time, end_time, project_id, keyword, user, deleted=deleted)
    temp_agent_fee = normal_agent_fee if user.level == 'normal' else all_agent_fee
    if not real_fee:
        real_fee = 0
    if not temp_agent_fee:
        temp_agent_fee = 0
    all_profit_fee = tools.format_fee(float(real_fee - temp_agent_fee))
    return all_profit_fee, tools.format_fee(float(temp_agent_fee))


def get_order_download_service(start_time, end_time, project_id, keyword, user, current_page, page_size, deleted=0, label='download'):
    """
    导出excel 数据
    :param start_time:
    :param end_time:
    :param project_id:
    :param keyword:
    :param user:
    :param current_page:
    :param page_size:
    :param deleted:
    :param label:
    :return:
    """
    order_obj_list = get_order_list_model(start_time, end_time, project_id, keyword, user, current_page,
                                                page_size, deleted=deleted, label=label)

    header_list = [
        u'订单id', u'商品名称', u'代理金额', u'出售金额', u'支付金额', u'利润', u'支付方式', u'收件人姓名',
        u'收件人地址', u'收件人手机号', u'创建时间'
    ]
    content_list = list()
    for order_obj in order_obj_list:
        project_obj = order_obj.project_obj
        agent_fee = tools.format_fee(project_obj.all_agent_fee) if g.user.level == 'all' else tools.format_fee(
            project_obj.normal_agent_fee)
        profit_fee = tools.format_fee(order_obj.real_fee) - agent_fee
        selling_fee = tools.format_fee(project_obj.selling_fee)
        _real_fee = tools.format_fee(order_obj.real_fee)
        pay_type = u'微信' if order_obj.pay_type == 'wechat_pay' else u'支付宝'
        temp_content_list = [
            order_obj.id, project_obj.name, agent_fee, selling_fee, _real_fee, profit_fee, pay_type,
            order_obj.name, order_obj.address, order_obj.phone, order_obj.create_time.strftime(DATE_TIME_FORMAT)
        ]
        content_list.append(temp_content_list)
    return header_list, content_list
