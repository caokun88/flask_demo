#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from flask import request, render_template, redirect, url_for
from flask_login import login_required

from utils import tools, decorator
from project import project_app
import service

from utils.respone_message import ok, bad_request


@project_app.route('/list/')
@login_required
@decorator.require_permission
def project_list_view():
    project_list = service.get_project_list(request.host_url)
    return render_template('admin/project_list.html', project_list=project_list)


@project_app.route('/add/', methods=['POST', 'GET'])
@project_app.route('/modify/<int:project_id>', methods=['POST', 'GET'])
@login_required
@decorator.require_permission
def project_add_view(project_id=None):
    if request.method == 'POST':
        name = request.form.get('name')
        agent_fee = request.form.get('agent_fee')
        selling_fee = request.form.get('selling_fee')
        file = request.files.get('icon')
        order_index = request.form.get('order_index')
        if file:
            icon = tools.upload_file(file, 'upload')
        else:
            icon = ''
        msg = service.add_or_modify_project(name, agent_fee, selling_fee, icon, order_index, project_id)
        if msg == 1:
            return redirect(url_for('project.project_list_view'))
        elif msg == 2:
            return u'系统错误'
        else:
            return u'参数错误'
    else:
        project_info = service.get_project(request.host_url, project_id)
        if isinstance(project_info, (int, long)):
            return bad_request()
        return render_template('admin/project_add.html', **project_info)

