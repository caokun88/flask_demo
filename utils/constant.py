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


# 微信相关

ACCESS_TOKEN_KEY = 'common_access_token'
TIMEOUT_ACCESS_TOKEN = 7000
JSAPI_TICKET_KEY = 'jsapi_ticket'
TIMEOUT_JSAPI_TICKET = 7000

WECHAT_TOKEN = ''

PAY_DICT = {
    'app_id': '',
    'secret': '',
    'mchid': '',
    'key': '',
    'ip': '',
    'pay_template_id': ''
}

DICT = {
    'app_id': 'wx23d18fcf079cb4c4',
    'secret': 'de0bd67ab3c763e0f274f7fa394ea4d0',
    'token': 'caokun'
}

API_URL_DICT = {
    'unified_order_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder',
    'pay_callback_url': 'http://xxxx/pay/notify/',
    'refund_url': 'https://api.mch.weixin.qq.com/secapi/pay/refund',
    'jsapi_ticket_url': 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi',
    'access_token_url': 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}',
    'create_menu_url': 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}',
    'web_access_token_url': 'https://api.weixin.qq.com/sns/oauth2/access_token?'
                            'appid={}&secret={}&code={}&grant_type=authorization_code',
    'web_user_info_url': 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN ',
    'user_info_url': 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN',
    'upload_multi_media_temp_url': 'http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}',
    'upload_multi_media_permanent_url': 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={}&type={}',
    'create_qrcode_url': 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}',
}

# 创建菜单
CLICK_CONTACT_CUSTOMER_KEY = 'contact-1'
CLICK_DICT = {
    CLICK_CONTACT_CUSTOMER_KEY: "如有问题，可联系-小蕊（微信号：kunrui_1314，电话：18810433987）"
}
DEFINE_MENU = {
    "button": [
        {
            "name": "A类",
            "sub_button": [
                {
                    "type": "view",
                    "name": "a-1",
                    "url": "http://www.baidu.com"
                },
                {
                    "type": "view",
                    "name": "a-2",
                    "url": "http://www.baidu.com"
                },
            ]
        },
        {
            "name": "B类",
            "sub_button": [
                {
                    "type": "view",
                    "name": "b-1",
                    "url": "http://www.baidu.com"
                },
                {
                    "type": "view",
                    "name": "b-2",
                    "url": "http://www.baidu.com"
                }
            ]
        },
        {
            "name": "C类",
            "sub_button": [
                {
                    "type": "view",
                    "name": "c-1",
                    "url": "http://www.baidu.com"
                },
                {
                    "type": "view",
                    "name": "c-2",
                    "url": "http://www.baidu.com"
                },
                {
                    "type": "click",
                    "name": "联系小蕊",
                    "key": CLICK_CONTACT_CUSTOMER_KEY
                }
            ]
        }
    ]
}