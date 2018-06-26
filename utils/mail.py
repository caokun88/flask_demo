#!/usr/bin/env python
# coding=utf8

"""
create on 2017-09-07
@author: cao kun
"""

import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import requests


EMAIL_HOST = 'smtp.qq.com'
EMAIL_USER = "1312637340@qq.com"
EMAIL_PASS = "thayjdbvoaltijef"


def send_mail(mail_to, subject='', content='', html_content='', file_paths=None, http_links=None):
    try:
        me = ("%s<" + EMAIL_USER + ">") % Header(u"颐和果园鲜果时光", "utf-8")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ','.join(mail_to)

        if content:
            msg.attach(MIMEText(content, 'plain', 'utf8'))
        if html_content:
            msg.attach((MIMEText(html_content, 'html', 'utf8')))

        if file_paths:
            for f in file_paths:
                f_name = f.split(r'/')[-1] if f.split(r'/') else f
                attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf8')
                attach['Content-Type'] = 'application/octet-stream'
                attach.add_header('Content-Disposition', 'attachment',
                                  filename='{}'.format(f_name.encode('UTF-8')))
                msg.attach(attach)

        if http_links:
            for l in http_links:
                f_name = l.split('filename=')[-1] if l.split('filename') else ''
                attach = MIMEText(requests.get(l).content, 'base64', 'utf8')
                attach['Content-Type'] = 'application/octet-stream'
                attach.add_header('Content-Disposition', 'attachment',
                                  filename='=?utf-8?b?' + base64.b64encode(f_name.encode('UTF-8')) + '?=')

        server = smtplib.SMTP()
        server.connect(EMAIL_HOST, 25)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(me, mail_to, msg=msg.as_string())
        server.quit()
    except Exception as e:
        print e
        return False
    return True


# if __name__ == '__main__':
#     send_mail(['caokun@xfz.cn'], subject=u'本地测试一下', content=u'本地测试')