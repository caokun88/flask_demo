#!/usr/bin/env python
# coding=utf8

import json
import hashlib
import random
import string
import time

import xmltodict
from bs4 import BeautifulSoup, CData
from constant import PAY_DICT, DICT


def get_wechat_pay_sign(params_dict):
    """
    微信关于支付生成的sign签名
    :param params_dict: 需要参加签名的数据
    :return: sign
    :rtype: str
    """
    keys = params_dict.keys()
    keys.sort()
    sign_str_arr = []
    for key in keys:
        if params_dict[key]:
            if isinstance(params_dict[key], int):
                value = str(params_dict[key])
            else:
                value = params_dict[key].encode("utf-8")
            sign_str_arr.append("=".join([key, value]))
    sign_str_arr.append("=".join(["key", PAY_DICT['key']]))
    sign_str = "&".join(sign_str_arr)
    sign = hashlib.md5(sign_str).hexdigest().upper()
    return sign


def check_from_wechat_signature(signature, timestamp, nonce):
    """
    验证是否是来自微信服务器
    :param signature:
    :param timestamp:
    :param nonce:
    :return: bool
    """
    info_str = ''.join(sorted([DICT['token'], timestamp, nonce]))
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


def get_dict_from_xml2(xml_str):
    try:
        return json.loads(json.dumps(xmltodict.parse(xml_str)))
    except Exception as e:
        return {}


def check_xml_sign(xml):
    """
    校验sign
    :param xml: xml
    :rtype: bool
    """
    data = get_dict_from_xml(xml)
    sign = data.pop('sign', None)
    x_sign = get_wechat_pay_sign(data)
    return x_sign == sign


def generate_nonce_str(length=32):
    """
    生成length位的随机字符串，默认32位
    :return: nonce_str
    :rtype: str
    """
    template_str = string.ascii_letters + string.ascii_letters
    nonce_str = ''.join([random.choice(template_str) for _ in range(length)])
    return nonce_str


class Sign:

    """微信分享用到的sign"""

    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'noncestr': self.__create_nonce_str(),
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
