#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

from flask import request, render_template

from utils import tools
from project import project_app
import service

from utils.respone_message import ok


@project_app.route('/list/')
def project_list_view():
    project_list = service.get_project_list()
    return ok(data={'project_list': project_list})


@project_app.route('/add/', methods=['POST', 'GET'])
def project_add_view():
    if request.method == 'POST':
        name = request.form.get('name')
        agent_fee = request.form.get('agent_fee')
        selling_fee = request.form.get('agent_fee')
        file = request.files.get('icon')
        order_index = request.form.get('order_index')
        print file.filename
        filename = tools.upload_file(file, 'upload')
        return u'name: {}'.format(name)
    else:
        return render_template('project_add.html')

