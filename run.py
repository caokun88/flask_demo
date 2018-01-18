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
from wechat.views import wechat_app
from frontend.index.views import frontend_app

app.register_blueprint(index_app, url_prefix='/admin')
app.register_blueprint(test_app, url_prefix='/test')
app.register_blueprint(project_app, url_prefix='/admin/project')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(order_app, url_prefix='/admin/order')
app.register_blueprint(wechat_app, url_prefix='/admin/wechat')

app.register_blueprint(frontend_app)


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def page_not_found_view(e):
    return render_template('error/404.html')


@app.route('/MP_verify_59WJCaIi0dtv1Qoe.txt/')
def wechat_js_file_view():

    return send_from_directory(static_dir, 'MP_verify_59WJCaIi0dtv1Qoe.txt', as_attachment=True)


@app.context_processor
def global_menu():
    try:
        role_obj = g.user.role_obj
        is_show = lambda role: True if g.user.role_obj.role == 'super' or g.user.role_obj.role == role else False
    except Exception as e:
        is_show = lambda role: False
    menu_list = [
        {
            'parent_name': u'用户管理',
            'sub_list': [
                {'name': u'添加用户', 'url': url_for('auth.register_view'), 'is_show': is_show('super')},
                {'name': u'用户列表', 'url': url_for('auth.user_list_view'), 'is_show': is_show('super')},
                {'name': u'退出', 'url': url_for('auth.logout_view'), 'is_show': is_show('user')}
            ]
        },
        {
            'parent_name': u'商品管理',
            'sub_list': [
                {'name': u'添加商品', 'url': url_for('project.project_add_view'), 'is_show': is_show('super')},
                {'name': u'商品列表', 'url': url_for('project.project_list_view'), 'is_show': is_show('user')},
            ]
        },
        {
            'parent_name': u'订单管理',
            'sub_list': [
                {'name': u'添加订单', 'url': url_for('order.order_add_view'), 'is_show': is_show('user')},
                {'name': u'订单列表', 'url': url_for('order.order_list_view'), 'is_show': is_show('user')},
            ]
        }
    ]
    return {'menu_list': menu_list, 'user': g.user}


if __name__ == '__main__':

    @app.route('/static/upload/<path:filename>')
    def show_img_file(filename):
        return send_from_directory(os.path.join(static_dir, 'upload'), filename)

    @app.route('/static/<filename>')
    def show_favicon_file(filename):
        return send_from_directory(static_dir, filename)


    @app.route('/static/js/<path:filename>')
    def show_js_file(filename):
        return send_from_directory(os.path.join(static_dir, 'js'), filename)


    @app.route('/static/css/<path:filename>')
    def show_css_file(filename):
        return send_from_directory(os.path.join(static_dir, 'css'), filename)


    app.run(host='0.0.0.0', port=5000, debug=app.debug)
