#!/usr/bin/env python
# coding=utf8

import hashlib
import random
import string
import time

from bs4 import BeautifulSoup, CData

APP_ID = 'wx23d18fcf079cb4c4'
APP_SECRET = 'de0bd67ab3c763e0f274f7fa394ea4d0'
WECHAT_CHECK_TOKEN = 'caokun'
CLICK_CONTACT_CUSTOMER_KEY = 'contact-1'
CLICK_DICT = {
    CLICK_CONTACT_CUSTOMER_KEY: "如有问题，可联系-小蕊（微信号：kunrui_1314，电话：18810433987）"
}




def check_from_wechat_signature(signature, timestamp, nonce):
    """
    验证是否是来自微信服务器
    :param signature:
    :param timestamp:
    :param nonce:
    :return: bool
    """
    info_str = ''.join(sorted([WECHAT_CHECK_TOKEN, timestamp, nonce]))
    hash_str = hashlib.sha1(info_str).hexdigest()
    if hash_str == signature:
        return True
    return False


def get_xml_from_dict(params_dict):
    """
    由字典转为xml字符串
    :param params_dict: 字典
    :return: xml_str
    :rtype: str
    """
    soup = BeautifulSoup(features="xml")
    xml = soup.new_tag("xml")
    for k, v in params_dict.items():
        tag = soup.new_tag(k)
        if isinstance(v, int):
            tag.append(soup.new_string(str(v)))
        elif isinstance(v, (str, unicode)):
            tag.append(CData(v))
        else:
            for k1, v1 in v.items():
                tag1 = soup.new_tag(k1)
                if isinstance(v1, int):
                    tag1.append(soup.new_string(str(v1)))
                elif isinstance(v1, (str, unicode)):
                    tag1.append(CData(v1))
            tag.append(tag1)
        xml.append(tag)
    return str(xml)


def get_dict_from_xml(xml_str):
    """
    由xml字符串转为dict
    :param xml_str: xml字符串
    :return: data
    :rtype: dict
    """
    soup = BeautifulSoup(xml_str, "xml")
    data = dict()
    for item in soup.find("xml").children:
        if item.name:
            data[item.name] = item.string
    return data


class Sign:

    """微信分享用到的sign"""

    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        nonce_str = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print nonce_str
        self.ret['signature'] = hashlib.sha1(nonce_str).hexdigest()
        return self.ret
