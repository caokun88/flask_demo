#!/usr/bin/env python
# coding=utf8

"""
create on 2017-11-23
@author: cao kun
"""

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
import urllib
import base64

from flask import request, render_template, session, redirect, url_for
from settings import csrf, redis_conn
from wechat import wechat_app
from utils.constant import CLICK_DICT, DICT
from utils.wechat_api import api_get_js_ticket, api_get_web_access_token, api_get_web_user_info
from utils.respone_message import ok
from utils.wechat_tools import check_from_wechat_signature, get_xml_from_dict, get_dict_from_xml, Sign, \
    get_dict_from_xml2


@csrf.exempt
@wechat_app.route('/callback/', methods=['GET', 'POST'])
def callback_view():
    signature = request.values.get('signature', '')
    timestamp = request.values.get('timestamp', '')
    nonce = request.values.get('nonce', '')
    echo_str = request.values.get("echostr", '')
    status = check_from_wechat_signature(signature, timestamp, nonce)
    if request.method == 'GET':
        if status:
            return echo_str
        return 'not weixin service request'
    else:
        if status:
            xml_str = request.data
            print xml_str
            # dict_data = get_dict_from_xml(xml_str)
            dict_data = get_dict_from_xml2(xml_str)
            msg_type = dict_data.get('MsgType')
            event = dict_data.get('Event')
            openid = dict_data.get('FromUserName')
            dev_wx = dict_data.get('ToUserName')
            event_key = dict_data.get('EventKey', '')
            ticket = dict_data.get('Ticket')
            resp_data = {
                'ToUserName': openid, 'FromUserName': dev_wx, 'CreateTime': int(time.time()), 'MsgType': msg_type,
            }
            if msg_type == 'event':
                print event
                if event in ['subscribe']:
                    # 关注后推送消息
                    if event_key and ticket:
                        # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                        if event_key.startswith('qrscene_'):
                            resp_data['Content'] = u'你是通过扫描带参数的二维码进来的, 你之前未关注过“我”，参数是：%s' % \
                                                   event_key.replace('qrscene_', '')
                        # else:
                        #     resp_data['Content'] = u'你是通过扫描带参数的二维码进来的, 你之前关注过“我”，参数是：%s' % event_key
                    else:
                        # 搜索名称关注
                        resp_data['Content'] = u"欢迎关注"
                    resp_data['MsgType'] = 'text'
                    xml_str = get_xml_from_dict(resp_data)
                    return xml_str
                elif event in ['unsubscribe']:
                    # 修改表状态
                    pass
                elif event in ['SCAN']:
                    # 用户已关注时，扫描带参数二维码事件
                    resp_data['MsgType'] = 'text'
                    if event_key.startswith('qrscene_'):
                        resp_data['Content'] = u'你是通过扫描带参数的二维码进来的, 你之前未关注过“我”，参数是：%s' % event_key.replace('qrscene_', '')
                    else:
                        resp_data['Content'] = u'你是通过扫描带参数的二维码进来的, 你之前关注过“我”，参数是：%s' % event_key
                elif event in ['TEMPLATESENDJOBFINISH']:
                    # 模板消息推送事件
                    if dict_data.get('Status') == 'success':
                        # 成功
                        pass
                    elif dict_data.get('Status') == 'failed:user block':
                        # 用户设置拒绝接收公众号消息
                        pass
                    else:
                        # 由于其他原因失败时
                        pass
                elif event in ['CLICK', 'VIEW']:
                    if event == 'CLICK':
                        # 自定义菜单点击
                        resp_data['Content'] = CLICK_DICT[event_key]
                        resp_data['MsgType'] = 'text'
                    else:
                        # 自定义菜单跳转链接
                        pass
            else:
                if msg_type == 'text':
                    resp_data['Content'] = dict_data['Content']
                    print resp_data
                elif msg_type == 'image':
                    resp_data['Image'] = {"MediaId": dict_data['MediaId']}
                elif msg_type == 'voice':
                    resp_data['Voice'] = {"MediaId": dict_data['MediaId']}
                elif msg_type == 'location':
                    resp_data['Content'] = u'你在：' + dict_data['Label']
                    resp_data['MsgType'] = 'text'
                elif msg_type == 'video':
                    resp_data['Content'] = u"你发送的是视频消息，对吗？"
                    resp_data['MsgType'] = 'text'
            xml_str = get_xml_from_dict(resp_data)
            return xml_str
    return ''


@wechat_app.route('/share/')
def share_view():
    print request.url_root
    return render_template('wechat/share.html')


@wechat_app.route('/api/sign/', methods=['POST', 'GET'])
def api_wechat_sign_view():
    """
    分享的sign
    :return:
    """
    url = request.values.get('url')
    jsapi_ticket = api_get_js_ticket()
    sign_obj = Sign(jsapi_ticket, url)
    sign_info = sign_obj.sign()
    sign_info['app_id'] = DICT['app_id']
    sign_info.pop('jsapi_ticket', '')
    return ok(data=sign_info)


@wechat_app.route('/auth-login-after/')
def auth_login_after_view():
    if not session.get('wechat_nickname'):
        # code_url = url_for('wechat.auth_login_code_view')
        encode_url = urllib.quote('{}wechat/auth-login-code/'.format(request.url_root))
        state = base64.b64encode(request.url)
        redirect_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&' \
                       'response_type=code&scope=snsapi_userinfo&state={}#wechat_redirect'.format(
            DICT['app_id'], encode_url, state
        )
        return redirect(redirect_url)
    return render_template('wechat/auth_login_after.html', **{'nickname': session.get('wechat_nickname').encode("raw_unicode_escape")})


@wechat_app.route('/auth-login-code/')
def auth_login_code_view():
    code = request.values.get('code')
    if code:
        resp_dict = api_get_web_access_token(code)
        access_token = resp_dict.get('access_token', '')
        openid = resp_dict.get('openid', '')
        # 拉取用户信息
        user_info = api_get_web_user_info(access_token, openid)
        print user_info
        if 'nickname' in user_info:
            session['wechat_nickname'] = user_info.get('nickname')
    else:
        session['wechat_nickname'] = 'ck'
    return redirect(url_for('wechat.auth_login_after_view'))
