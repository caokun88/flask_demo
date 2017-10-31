#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-13
@author: cao kun
"""

import datetime


__add_time = lambda month: datetime.datetime.now() + datetime.timedelta(month)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_TIME_FORMAT_2 = '%Y-%m-%d_%H:%M:%S'

DATE_FORMAT = '%Y-%m-%d'

CURRENT_PAGE = 1

PAGE_SIZE = 10

AGENT_LEVEL = ('normal', 'all')

AGENT_DICT = {'normal': u'普通代理', 'all': u'总代理'}

EXPIRE_TIME_DICT = {'one': __add_time, 'three': __add_time, 'six': __add_time, 'twelve': __add_time}

MONTH_LIST = ('one', 'three', 'six', 'twelve')

MONTH_DICT = {'one': 30, 'three': 91, 'six': 182, 'twelve': 365}
