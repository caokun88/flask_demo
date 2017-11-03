#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

import datetime
from StringIO import StringIO

from flask import redirect, url_for, g, request, render_template, flash, session, make_response
from flask_login import logout_user, login_user, current_user, login_required
from auth import lm, auth_app
from model import User, Role, db
from utils import decorator, captcha
from settings import csrf
from utils.respone_message import bad_request, expire_request, ok, error
from utils import tools
from utils.constant import AGENT_LEVEL, MONTH_LIST, MONTH_DICT, AGENT_DICT
import service


@lm.user_loader
def load_user(id):
    return User.query.get(id)


@auth_app.route('/logout/')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index.index_view'))


@auth_app.route('/skip/')
def skip_view():
    return render_template('skip.html')


@auth_app.route('/captcha/')
def captcha_view():
    img, range_str = captcha.generate_captcha()
    session['captcha_code'] = range_str.upper()
    buf = StringIO()
    img.save(buf, 'png')
    response = make_response(buf.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@auth_app.route('/login/', methods=['POST', 'GET'])
def login_view():
    next_url = request.args.get('next', '')
    if g.user is not None and g.user.is_authenticated:
        return redirect(next_url)
    if request.method == 'POST':
        nickname = request.form.get('nickname', '')
        password = request.form.get('password', '')
        captcha = request.form.get('captcha', '').upper()
        old_user_obj = service.check_user_exists(nickname)
        if old_user_obj and old_user_obj.expire_time:
            if old_user_obj.expire_time <= datetime.datetime.now():
                return expire_request()
        if captcha and captcha != session.get('captcha_code') or not captcha:
            flash(u'验证码错误')
            return redirect(url_for('auth.skip_view'))
        user = User.query.filter_by(nickname=nickname).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            session.permanent = True  # 只要用户活跃，session就是永久的
            return redirect(next_url or url_for('index.index_view'))
        else:
            flash(u'失败')
            return redirect(url_for('auth.skip_view'))
    else:
        return render_template('login.html')


@auth_app.route('/add/user/', methods=['POST', 'GET'])
@login_required
@decorator.require_permission
def register_view():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '')
        real_name = request.form.get('real_name', '')
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        email = request.form.get('email', '')
        wechat = request.form.get('wechat', '')
        role_id = request.form.get('role_id', '')
        if not all([nickname, password, password_confirm, email]):
            flash(u'nickname, password, password_confirm, email both not null')
        if password_confirm != password:
            flash(u'两次密码不一致')
        role_obj = Role.query.filter_by(id=role_id).first()
        if not role_obj:
            flash(u'角色id不存在')
        old_user_obj = service.check_user_exists(nickname)
        if not old_user_obj:
            user = User(nickname=nickname, email=email, wechat=wechat, role_id=role_id, real_name=real_name)
            user.expire_time = tools.get_n_day_before(7)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index.index_view'))
            flash(u'添加成功')
        else:
            flash(u'用户名存在')
    else:
        return render_template('register.html')


@auth_app.route('/user/list/', methods=['GET'])
@login_required
@decorator.require_permission
def user_list_view():
    nickname = request.args.get('nickname', '')
    current_page = request.args.get('current_page', 1)
    page_size = request.args.get('page_size', 10)
    try:
        current_page = int(current_page)
        page_size = int(page_size)
    except Exception as e:
        return bad_request()
    user_list, page = service.get_user_list(nickname, current_page, page_size)
    resp_data = {
        'user_list': user_list, 'page': page, 'nickname': nickname, 'agent_level_list': AGENT_LEVEL,
        'month_dict': MONTH_DICT, 'month_list': MONTH_LIST, 'agent_level_dict': AGENT_DICT
    }
    return render_template('admin/user_list.html', **resp_data)


@auth_app.route('/modify/<int:user_id>/user/', methods=['POST'])
@login_required
@decorator.require_permission
def modify_user_view(user_id):
    level = request.form.get('level')
    expire_time_str = request.form.get('expire_time_str')
    msg = service.modify_user(user_id, level, expire_time_str)
    if msg == 3:
        return bad_request()
    elif msg == 1:
        return ok()
    return error()
