#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-17
@author: cao kun
"""

from StringIO import StringIO

from flask import redirect, url_for, g, request, render_template, flash, session, make_response
from flask_login import logout_user, login_user, current_user, login_required
from auth import lm, auth_app
from model import User, Role, db
from utils import decorator, captcha
from settings import csrf


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
    img.save(buf, 'JPEG', quality=60)
    buffer_str = buf.getvalue()
    response = make_response(buffer_str)
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
        if captcha and captcha != session.get('captcha_code') or not captcha:
            flash(u'验证码错误')
            return redirect(url_for('auth.skip_view'))
        user = User.query.filter_by(nickname=nickname).first()
        if user is not None and user.verify_password(password):
            login_user(user)
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
        user = User(nickname=nickname, email=email, wechat=wechat, role_id=role_id, real_name=real_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index.index_view'))
        flash(u'添加成功')
    else:
        return render_template('register.html')