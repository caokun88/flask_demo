#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

from flask import request, render_template, redirect, url_for
from flask_login import login_required

from order import order_app
from utils import decorator
from utils.respone_message import ok
import service
from project import service as project_service


@order_app.route('/list/')
@login_required
@decorator.require_permission
def order_list_view():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    order_list = service.get_order_list_service(start_time, end_time)
    return render_template('order_list.html', order_list=order_list)


@order_app.route('/add/', methods=['POST', 'GET'])
@login_required
@decorator.require_permission
def order_add_view():
    if request.method == 'POST':
        real_fee = request.form.get('real_fee')
        pay_type = request.form.get('pay_type')
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        project_id = request.form.get('project_id')
        service.add_order_model(project_id, real_fee, name, address, phone, pay_type)
        return redirect(url_for('order.order_list_view'))
    else:
        project_list = project_service.get_project_list(request.host_url)
        return render_template('order_add.html', project_list=project_list)
