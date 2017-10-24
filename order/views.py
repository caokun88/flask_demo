#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

import datetime

from flask import request, render_template, redirect, url_for, g
from flask_login import login_required

from order import order_app
from utils import decorator
from utils.respone_message import ok
import service
from project import service as project_service
from utils.constant import DATE_FORMAT


@order_app.route('/list/')
@login_required
@decorator.require_permission
def order_list_view():
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    if not any([start_time, end_time]):
        start_time = datetime.datetime.now().strftime(DATE_FORMAT)
    order_list, total_count, total_flowing_fee, total_profit_fee = \
        service.get_order_list_service(start_time, end_time, g.user)
    resp_data = {
        'order_list': order_list, 'start_time': start_time, 'end_time': end_time, 'total_count': total_count,
        'total_flowing_fee': total_flowing_fee, 'total_profit_fee': total_profit_fee
    }
    return render_template('admin/order_list.html', **resp_data)


@order_app.route('/add/', methods=['POST', 'GET'])
@order_app.route('/modify/<int:order_id>/', methods=['POST', 'GET'])
@login_required
@decorator.require_permission
def order_add_view(order_id=None):
    if request.method == 'POST':
        real_fee = request.form.get('real_fee')
        pay_type = request.form.get('pay_type')
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        project_id = request.form.get('project_id')
        if all([real_fee, pay_type, name, address, phone, project_id]):
            service.add_order_model(order_id, project_id, real_fee, name, address, phone, pay_type, g.user)
        return redirect(url_for('order.order_list_view'))
    else:
        project_list = project_service.get_project_list(request.host_url)
        order_info = service.get_order_info(order_id)
        print order_info
        return render_template('admin/order_add.html', project_list=project_list, order_info=order_info)


@order_app.route('/delete/<int:order_id>/', methods=['POST'])
@login_required
@decorator.require_permission
def order_deleted_view(order_id):
    service.delete_order_model(order_id, g.user)
    return ok()
