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
from utils.respone_message import ok, bad_request
import service
from project import service as project_service
from utils.constant import DATE_FORMAT
from utils import tools


@order_app.route('/list/')
@login_required
def order_list_view():
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    project_id = request.args.get('project_id', '')
    keyword = request.args.get('keyword', '')
    current_page = request.args.get('current_page', 1)
    page_size = request.args.get('page_size', 10)
    try:
        current_page = int(current_page)
        page_size = int(page_size)
    except Exception as e:
        return bad_request()
    if not any([start_time, end_time]):
        start_time = datetime.datetime.now().strftime(DATE_FORMAT)
    order_list, page, total_flowing_fee, total_profit_fee = \
        service.get_order_list_service(start_time, end_time, project_id, keyword, g.user, current_page, page_size)
    all_profit_fee, all_agent_fee = service.order_statics_service(start_time, end_time, project_id, keyword, g.user)
    project_list = project_service.get_project_list(request.host_url)
    resp_data = {
        'order_list': order_list, 'start_time': start_time, 'end_time': end_time, 'page': page,
        'total_flowing_fee': total_flowing_fee, 'total_profit_fee': total_profit_fee, 'project_list': project_list,
        'project_id': project_id, 'keyword': keyword, 'all_profit_fee': all_profit_fee, 'all_agent_fee': all_agent_fee
    }
    
    return render_template('admin/order_list.html', **resp_data)


@order_app.route('/add/', methods=['POST', 'GET'])
@order_app.route('/modify/<int:order_id>/', methods=['POST', 'GET'])
@login_required
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
        return render_template('admin/order_add.html', project_list=project_list, order_info=order_info)


@order_app.route('/delete/<int:order_id>/', methods=['POST'])
@login_required
def order_deleted_view(order_id):
    service.delete_order_model(order_id, g.user)
    return ok()


@order_app.route('/download/')
@login_required
def order_download_view():
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    project_id = request.args.get('project_id', '')
    keyword = request.args.get('keyword', '')
    current_page = request.args.get('current_page', 1)
    page_size = request.args.get('page_size', 10)
    try:
        current_page = int(current_page)
        page_size = int(page_size)
    except Exception as e:
        return bad_request()
    if not any([start_time, end_time]):
        start_time = datetime.datetime.now().strftime(DATE_FORMAT)
    header_list, content_list = service.get_order_download_service(start_time, end_time, project_id, keyword, g.user, current_page, page_size)
    response = tools.download_excel(header_list, content_list)
    return response
