#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-25
@author: cao kun
"""

import modules
from utils.constant import CURRENT_PAGE, PAGE_SIZE, DATE_TIME_FORMAT


def get_user_list(nickname=None, current_page=CURRENT_PAGE, page_size=PAGE_SIZE):
    """
    用户列表
    :param nickname: 用户登录名
    :param current_page:
    :param page_size:
    :return:
    """
    user_obj_list, page = modules.get_user_list(nickname, current_page, page_size)
    user_list = list()
    for user_obj in user_obj_list:
        user_list.append({
            'id': user_obj.id,
            'nickname': user_obj.nickname,
            'real_name': user_obj.real_name,
            'level': u'普代' if user_obj.level == 'normal' else u'总代',
            'expire_time': user_obj.expire_time.strftime(DATE_TIME_FORMAT) if user_obj.expire_time else u'永久',
            'wechat': user_obj.wechat,
            'email': user_obj.email,
            'login_count': user_obj.login_count,
            'login_last_time': user_obj.login_last_time.strftime(DATE_TIME_FORMAT) if user_obj.login_last_time else '',
            'login_last_ip': user_obj.login_last_ip,
            'create_time': user_obj.c_time.strftime(DATE_TIME_FORMAT)
        })
    return user_list, page


def check_user_exists(nickname):
    """
    检测此登录名的用户是否存在
    :param nickname:
    :return:
    """
    old_user_obj = modules.check_user_exists(nickname)
    return old_user_obj


def get_user_by_id(user_id):
    """
    检测此登录名的用户是否存在
    :param user_id: 用户id
    :return:
    """
    old_user_obj = modules.get_user_by_id(user_id)
    return old_user_obj


def modify_user(user_id, level=None, expire_time_str=None):
    """
    修改用户代理等级和过期时间
    :param user_id:
    :param level:
    :param expire_time_str:
    :return:
    """
    msg = modules.modify_user(user_id, level=level, expire_time_str=expire_time_str)
    return msg
