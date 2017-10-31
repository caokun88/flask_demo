#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-31
@author: cao kun
"""

import time

from tasks import app


@app.task(queue='ck:celery:test')
def test_celery(x, y):
    time.sleep(5)
    return x + y
