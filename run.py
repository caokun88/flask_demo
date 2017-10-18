#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

import os

from flask import send_from_directory, g, url_for, render_template
from flask_login import current_user

from settings import app, static_dir
from index.views import index_app
from test_demo.views import test_app
from project.views import project_app
from auth.views import auth_app
from order.views import order_app

app.register_blueprint(index_app)
app.register_blueprint(test_app, url_prefix='/test')
app.register_blueprint(project_app, url_prefix='/project')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(order_app, url_prefix='/order')


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def page_not_found_view(e):
    return render_template('error/404.html')


@app.context_processor
def global_menu():
    menu_list = [
        {
            'parent_name': u'用户管理',
            'sub_list': [
                {'name': u'添加用户', 'url': url_for('auth.register_view')},
                {'name': u'退出', 'url': url_for('auth.logout_view')}
            ]
        },
        {
            'parent_name': u'商品管理',
            'sub_list': [
                {'name': u'添加商品', 'url': url_for('project.project_add_view')},
                {'name': u'商品列表', 'url': url_for('project.project_list_view')},
            ]
        },
        {
            'parent_name': u'订单管理',
            'sub_list': [
                {'name': u'添加订单', 'url': url_for('order.order_add_view')},
                {'name': u'订单列表', 'url': url_for('order.order_list_view')},
            ]
        }
    ]
    return {'menu_list': menu_list, 'user': g.user}


if __name__ == '__main__':

    @app.route('/static/upload/<path:filename>')
    def show_file(filename):
        return send_from_directory(os.path.join(static_dir, 'upload'), filename)
    app.run(host='0.0.0.0', port=5000, debug=app.debug)
