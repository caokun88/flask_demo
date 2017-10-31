#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-31
@author: cao kun
"""

from __future__ import absolute_import

from celery import Celery

app = Celery('my_task')

app.config_from_object('tasks.config')
