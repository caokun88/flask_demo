#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-25
@author: cao kun
"""

from model import db, User, Role
from utils.constant import CURRENT_PAGE, PAGE_SIZE
from utils import tools


def get_user_list(nickname=None, current_page=CURRENT_PAGE, page_size=PAGE_SIZE):
    """
    用户列表
    :param nickname: 用户的登录名
    :param current_page:
    :param page_size:
    :return:
    """
    user_obj_list = User.query.filter()
    if nickname:
        user_obj_list = user_obj_list.filter(User.nickname == nickname)
    total_count = user_obj_list.count()
    user_obj_list = user_obj_list.order_by(db.desc(User.id))
    if current_page and page_size:
        user_obj_list = user_obj_list.offset((current_page - 1) * page_size).limit(page_size)
    page = tools.get_page(current_page, page_size, total_count)
    return user_obj_list, page


def check_user_exists(nickname):
    """
    检测此登录名的用户是否存在
    :param nickname:
    :return: 存在 True 不存在 False
    """
    old_user_obj = User.query.filter(User.nickname == nickname).first()
    return old_user_obj
