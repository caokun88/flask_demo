#!/usr/bin/env python
# coding=utf-8


"""
fork 一个进程来做其他事儿, windows 系统不能用os.fork()
"""

import os
import sys

from utils.mail import send_mail


def run():
    print 'fork before'
    try:
        res = os.fork()
    except Exception as e:
        print e
        res = None
        sys.exit(1)
    if res == 0:
        print 'mail start'
        send_mail(['1312637340@qq.com'], subject=u'测试', content=u'fork 进程发邮件test')
        print 'success'
    else:
        print u'父进程ok'


if __name__ == '__main__':
    run()
