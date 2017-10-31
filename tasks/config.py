#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-31
@author: cao kun
"""

from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_IMPORTS = (
    'tasks.test',
)

# schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
#          'args': (5, 8)                           # 任务函数参数
#     },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task2.multiply',
#         'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
#         'args': (3, 7)                            # 任务函数参数
#     }
# }