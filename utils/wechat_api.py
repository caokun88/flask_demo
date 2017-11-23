# /usr/bin/env python
# coding=utf8

import json
import os

import requests

from settings import redis_conn
from constant import PAY_DICT, DICT, API_URL_DICT, TIMEOUT_ACCESS_TOKEN, ACCESS_TOKEN_KEY, JSAPI_TICKET_KEY, \
    DEFINE_MENU, TIMEOUT_JSAPI_TICKET
from utils.wechat_tools import get_xml_from_dict, generate_nonce_str


# 统一下单请求数据
data = {
    "appid": PAY_DICT["app_id"],
    "mch_id": PAY_DICT["mchid"],
    "nonce_str": generate_nonce_str(),
    "body": 'product_name',
    "out_trade_no": 'order_id',
    "total_fee": 'total_fee',
    "spbill_create_ip": PAY_DICT["ip"],
    "notify_url": API_URL_DICT["pay_callback_url"],
    "trade_type": 'trade_type',
    "product_id": 'product_id',
    'openid': 'openid'  # 如果有就用，没有就不用
}


def api_wechat_unified_order(param_dict):
    """
    微信统一下单
    :param param_dict: 下单数据字典
    :return: resp_dict
    :rtype: dict
    trade_type == native: code_url(这个是扫码支付的链接，需要自己转成二维码)
    trade_type == jsapi: 详细看文档
    trade_type = app: 详细看文档
    """
    url = API_URL_DICT['unified_order_url']
    req_xml = get_xml_from_dict(param_dict)
    resp_str = requests.post(url=url, data=req_xml)
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
        print e
    return resp_dict


refund_dict = {
    'appid': PAY_DICT["app_id"],
    'mch_id': PAY_DICT["mchid"],
    'out_trade_no': 'order_id',
    'nonce_str': generate_nonce_str(),
    'total_fee': 'int(total_fee)',
    'refund_fee': 'int(refund_fee)',
    'out_refund_no': "str(int(time.time())) + '_' + nonce_str"
}


def api_wechat_refund(param_dict):
    """
    微信退款api
    :param param_dict: 退款参数
    :return: resp_data
    :rtype: dict
    return_code == 'SUCCESS' and result_code == 'SUCCESS', 才是退款api成功，具体退款时间，看情况。
    """
    url = API_URL_DICT['refund_url']
    req_xml = get_xml_from_dict(param_dict)
    dir_name = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    cert_path = os.path.join(dir_name, r'wx_cert/apiclient_cert.pem')  # 证书cert
    cert_key_path = os.path.join(dir_name, r'wx_cert/apiclient_key.pem')  # 证书key
    resp_str = requests.post(url=url, data=req_xml, cert=(cert_path, cert_key_path))
    try:
        resp_data = resp_str.json()
    except Exception as e:
        resp_data = dict()
    return resp_data


def __api_get_access_token():
    """
    获取通用access_token
    :return: access_token
    :rtype: str
    """
    redis_access_token = redis_conn.get(ACCESS_TOKEN_KEY)
    if redis_access_token:
        return redis_access_token
    app_id, secret = DICT['app_id'], DICT['secret']
    url = API_URL_DICT['access_token_url']
    resp_str = requests.get(
        url=url.format(app_id, secret)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    if resp_dict:
        access_token = resp_dict['access_token']
        redis_conn.setex(ACCESS_TOKEN_KEY, TIMEOUT_ACCESS_TOKEN, access_token)
        return access_token
    else:
        return None


def api_create_menu(param_dict):
    """
    创建菜单api
    :param param_dict: 菜单内容
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['create_menu_url']
    access_token = __api_get_access_token()
    resp_str = requests.post(
        url=url.format(access_token),
        data=json.dumps(param_dict, ensure_ascii=False)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_send_template(product_name, openid, click_url):
    """
    发送模板消息api
    :param product_name: 产品名称
    :param openid: 接收模板消息的openid
    :param click_url: 点击跳转的url
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['']
    access_token = __api_get_access_token()
    data = {
        'first': {'value': '恭喜你购买成功！', 'color': '#173177'},
        'name': {"value": product_name},
        'remark': {'value': 'REMARK_TEXT'}
    }
    param_data = {
        'touser': openid,
        'template_id': PAY_DICT['pay_template_id'],
        'url': click_url,
        'data': data
    }
    resp_str = requests.post(
        url=url.format(access_token),
        data=json.dumps(param_data, ensure_ascii=False).encode('utf8')
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_web_access_token(code):
    """
    获取网页access_token和openid
    :param code: code
    :return: access_token, openid
    :rtype: str, str
    """
    url = API_URL_DICT['web_access_token_url']
    app_id, secret = DICT['app_id'], DICT['secret']
    resp_str = requests.get(
        url=url.format(app_id, secret, code)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_web_user_info(access_token, openid):
    """
    网页授权，获取用户基本信息api
    :param access_token: 网页授权access_token
    :param openid: 用户的openid
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['web_user_info_url']
    resp_str = requests.get(
        url=url.format(access_token, openid)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_user_info(openid):
    """
    获取用户的基本信息，包括是否关注过该公众号（订阅号或者服务号）
    :param openid: 用户的openid
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['user_info_url']
    access_token = __api_get_access_token()
    resp_str = requests.get(
        url=url.format(access_token, openid)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_temp_media_id(file_path=None, media_type='image'):
    """
    向微信服务器上传多媒体文件，返回可用的media_id（临时）
    :param file_path:
    :param media_type:
    :return:
    """
    url = API_URL_DICT['upload_multi_media_temp_url']
    access_token = __api_get_access_token()
    if file_path is None:
        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(file_path, 'static/images/kf.png')
    f = open(file_path, 'rb')
    resp_str = requests.post(
        url=url.format(access_token, media_type),
        files={'image': f}
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_permanent_media_id(file_path=None, media_type='image'):
    """
    向微信服务器上传多媒体文件，返回可用的media_id（永久）
    :param file_path:
    :param media_type:
    :return:
    """
    url = API_URL_DICT['upload_multi_media_permanent_url']
    access_token = __api_get_access_token()
    if file_path is None:
        file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(file_path, 'static/images/xfz.png')
    f = open(file_path, 'rb')
    resp_str = requests.post(
        url=url.format(access_token, media_type),
        files={'media': ('xfz.png', f, 'image/png')}
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def create_qr_scene(label):
    """
    创建临时二维码
    :return:
    """
    access_token = __api_get_access_token()
    resp_data = requests.post(
        url=API_URL_DICT['create_qrcode_url'].format(access_token),
        data=json.dumps({
            "expire_seconds": 3600, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": label}}
        })
    )
    try:
        resp_json = resp_data.json()
    except Exception as e:
        resp_json = dict()
    return resp_json


def create_define_menu():
    """
    创建自定义菜单
    :return: resp_json
    :rtype: dict
    """
    access_token = __api_get_access_token()
    resp_data = requests.post(
        url=API_URL_DICT['create_menu_url'].format(access_token),
        data=json.dumps(DEFINE_MENU, ensure_ascii=False).encode('utf8')
    )
    try:
        resp_json = resp_data.json()
    except Exception as e:
        resp_json = dict()
    return resp_json


def api_get_js_ticket():
    """
    获取jsapi_ticket
    :return:
    """
    jsapi_ticket = redis_conn.get(JSAPI_TICKET_KEY)
    if jsapi_ticket:
        return jsapi_ticket
    url = API_URL_DICT['jsapi_ticket_url']
    access_token = __api_get_access_token()
    resp_str = requests.get(
        url=url.format(access_token)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        print e
        resp_dict = dict()
    jsapi_ticket = resp_dict.get('ticket')
    if jsapi_ticket:
        redis_conn.setex(JSAPI_TICKET_KEY, TIMEOUT_JSAPI_TICKET, jsapi_ticket)
    return jsapi_ticket


if __name__ == '__main__':
    resp_dict = api_get_permanent_media_id()
    print resp_dict
