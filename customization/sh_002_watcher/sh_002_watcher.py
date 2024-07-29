#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""

import urllib
import urllib.parse
import pprint
import requests
import random
import string
import hashlib
import hmac
import warnings
import os
import json
import time
import datetime
import shelve
import argparse
from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# 忽略 SSL 警告
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

CURRENT_TIME = int(time.time() * 1000)  # 当前时间戳（毫秒）

SERVERLESS_CLIENT_SECRET = os.environ['SERVERLESS_CLIENT_SECRET']
SERVERLESS_SPACE_ID = os.environ['SERVERLESS_SPACE_ID']

SERVERLESS_ACCESS_TOKEN = 'QYD_SERVERLESS_ACCESS_TOKEN'
SIGN_INFO = 'QYD_SIGN_INFO'
API_ACCESS_TOKEN = 'QYD_API_ACCESS_TOKEN'
LOGIN_TOKEN = 'QYD_LOGIN_TOKEN'

PROXY = None


def save_date_to_local_file(filename: str, data: str):
    """
    数据缓存到本地文件
    """
    with open(f"./{filename}", 'w') as f:
        f.write(data)


def load_data_from_local_file(filename: str, expire_time: int, using_cached: bool = False):
    """
    从本地文件读取数据，若不存在或超时，则重新拉取
    """
    file_path = f"./{filename}"
    try:
        with open(file_path, 'r') as f:
            local_data = f.read().strip()
        # 获取文件的最后修改时间
        file_mod_time = os.path.getmtime(file_path)
        file_mod_date = datetime.datetime.fromtimestamp(file_mod_time)
        # 计算文件的年龄
        file_age_seconds = (datetime.datetime.now() - file_mod_date).seconds
        print(f"{file_path}: {file_mod_date}")
    except FileNotFoundError:
        if filename == LOGIN_TOKEN:
            raise Exception(f"import new LOGIN_ACCESS_TOKEN！！！！")
        print(f"not local file: {file_path}")
        local_data = ''
        file_age_seconds = 0

    if file_age_seconds > expire_time or not local_data or not using_cached:
        print(f"data is expired, getting new data for {filename}")
        if filename == SERVERLESS_ACCESS_TOKEN:
            new_data = get_serverless_access_token()
        elif filename == SIGN_INFO:
            serverless_access_token = get_serverless_access_token()
            new_data = get_sign_info_from_serverless(access_token=serverless_access_token)
        elif filename == API_ACCESS_TOKEN:
            sign_info = load_sign_info()
            new_data = get_api_access_token(sign_info=sign_info)
        elif filename == LOGIN_TOKEN:
            sign_info = load_sign_info()
            api_access_token = load_api_access_token()
            new_data = refresh_login_token(sign_info=sign_info,
                                           api_access_token=api_access_token,
                                           login_token=local_data)
        else:
            raise Exception(f"unknown filename {filename}")
        # 缓存数据
        if isinstance(new_data, dict):
            # 如果是字典，转换为JSON字符串
            data_str = json.dumps(new_data)
        else:
            data_str = new_data
        save_date_to_local_file(file_path, data_str)
        # 返回数据
        return new_data
    else:
        print(f"data is loaded by local file {filename}")
        try:
            # 尝试将字符串解析为字典
            result = json.loads(local_data)
            # 检查解析结果是否为字典
            return result
        except (json.JSONDecodeError, TypeError):
            # 如果解析失败，直接返回
            return local_data


def load_serverless_token(using_cached: bool = True):
    """
    加载云函数的token
    """
    return load_data_from_local_file(SERVERLESS_ACCESS_TOKEN, 500, using_cached)


def load_sign_info(using_cached: bool = True):
    """
    加载云函数的token
    """
    return load_data_from_local_file(SIGN_INFO, 6000, using_cached)


def load_api_access_token(using_cached: bool = True):
    """
    加载云函数的token
    """
    return load_data_from_local_file(API_ACCESS_TOKEN, 6000, using_cached)


def load_login_token(using_cached: bool = True):
    """
    加载云函数的token
    """
    return load_data_from_local_file(LOGIN_TOKEN, 4320000, using_cached)


def generate_nonce():
    timestamp = str(int(time.time() * 1000))  # current time in milliseconds
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    noncestr = f"{timestamp}{random_str}"
    return noncestr


nonce = generate_nonce()


def Ae(body, secret):
    """
    云函数的签名函数
    """
    # 1. 对字典按键排序
    sorted_items = sorted(body.items())
    # 2. 拼接成字符串，并进行 URL 编码
    query_string = '&'.join([f"{k}={str(v)}" for k, v in sorted_items if v])
    # 3. HMAC-MD5 签名
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.md5).hexdigest()
    return signature


def get_serverless_access_token():
    url = "https://api.next.bspapp.com/client"

    data = {
        "method": "serverless.auth.user.anonymousAuthorize",
        "params": "{}",
        "spaceId": SERVERLESS_SPACE_ID,
        "timestamp": CURRENT_TIME
    }
    pprint.pprint(data)
    serverless_sign = Ae(data, SERVERLESS_CLIENT_SECRET)
    # print(f"serverless_sign: {serverless_sign}")
    headers = {
        "Host": "api.next.bspapp.com",
        "xweb_xhr": "1",
        "x-serverless-sign": serverless_sign,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/"
                      "WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, proxies={"https": PROXY},
                                 timeout=5)
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("success"):
            access_token = response_json["data"]["accessToken"]
            return access_token
        else:
            raise Exception("Request was not successful: {}".format(response_json))
    else:
        raise Exception("Failed to get a valid response: HTTP {}".format(response.status_code))


def get_sign_info_from_serverless(access_token: str):
    """
    access_token:
    """
    url = "https://api.next.bspapp.com/client?"
    data = {
        "method": "serverless.function.runtime.invoke",
        "params": json.dumps({
            "functionTarget": "get-sign-info",
            "functionArgs": {
                "client_time": CURRENT_TIME,
                "device_id": CURRENT_TIME,
                "sign_key": "",
                "noncestr": nonce,
                "utm_source": "miniprogram",
                "utm_medium": "wechatapp",
                "app_version": "3.0.9",
                "latitude": 0,
                "longitude": 0,
                "access_token": "",
                "login_token": "",
                "url": "https://xapi.quyundong.com/Api/Cloud/getSignInfo",
                "clientInfo": {
                    "PLATFORM": "mp-weixin",
                    "OS": "mac",
                    "APPID": "__UNI__902073B",
                    "DEVICEID": CURRENT_TIME,
                    "scene": 1074,
                    "albumAuthorized": True,
                    "benchmarkLevel": -1,
                    "bluetoothEnabled": False,
                    "cameraAuthorized": True,
                    "locationAuthorized": True,
                    "locationEnabled": True,
                    "microphoneAuthorized": True,
                    "notificationAuthorized": True,
                    "notificationSoundEnabled": True,
                    "power": 100,
                    "safeArea": {
                        "bottom": 736,
                        "height": 736,
                        "left": 0,
                        "right": 414,
                        "top": 0,
                        "width": 414
                    },
                    "screenHeight": 736,
                    "screenWidth": 414,
                    "statusBarHeight": 0,
                    "theme": "light",
                    "wifiEnabled": True,
                    "windowHeight": 736,
                    "windowWidth": 414,
                    "enableDebug": False,
                    "devicePixelRatio": 2,
                    "deviceId": "17219164685639263029",
                    "safeAreaInsets": {
                        "top": 0,
                        "left": 0,
                        "right": 0,
                        "bottom": 0
                    },
                    "appId": "__UNI__902073B",
                    "appName": "趣运动(新)",
                    "appVersion": "1.0.0",
                    "appVersionCode": "100",
                    "appLanguage": "zh-Hans",
                    "uniCompileVersion": "3.99",
                    "uniRuntimeVersion": "3.99",
                    "uniPlatform": "mp-weixin",
                    "deviceBrand": "apple",
                    "deviceModel": "MacBookPro18,1",
                    "deviceType": "pc",
                    "osName": "mac",
                    "osVersion": "OS",
                    "hostTheme": "light",
                    "hostVersion": "3.8.8",
                    "hostLanguage": "zh-CN",
                    "hostName": "WeChat",
                    "hostSDKVersion": "3.3.5",
                    "hostFontSizeSetting": 15,
                    "windowTop": 0,
                    "windowBottom": 0,
                    "locale": "zh-Hans",
                    "LOCALE": "zh-Hans"
                }
            }
        }),
        "spaceId": SERVERLESS_SPACE_ID,
        "timestamp": CURRENT_TIME,
        "token": access_token
    }
    serverless_sign = Ae(data, SERVERLESS_CLIENT_SECRET)
    # print(f"serverless_sign: {serverless_sign}")
    headers = {
        "Host": "api.next.bspapp.com",
        "x-basement-token": access_token,
        "xweb_xhr": "1",
        "x-serverless-sign": serverless_sign,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) "
                      "NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, proxies={"https": PROXY},
                                 timeout=5)
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("success"):
            return response_json["data"]['result']['data']['data']
        else:
            raise Exception(response.text)
    else:
        raise Exception(response.text)


def generate_api_sign(body: dict, url: str, api_key: str):
    n = ""
    if url:
        # 假设 p 是某个已知的前缀
        p = "https://xapi.quyundong.com"
        n = url.split(f"{p}/")[1].replace("/", ":").lower()
    i = n
    if body:
        # 获取并排序键
        keys = sorted(body.keys())
        a = {}
        for key in keys:
            a[key] = body[key]
        # 生成查询字符串
        for key in a:
            i += f"{key}={urllib.parse.quote(str(a[key]))}&"
        # 拼接 api_key
        i += api_key
    print(i)
    return hashlib.sha256(i.encode('utf-8')).hexdigest()


def refresh_login_token(sign_info: dict, api_access_token: str, login_token: str):
    """
    获取业务接口的token
    # 60天过期一次
    """
    url = "https://xapi.quyundong.com/Api/User/refreshLoginToken"
    nonce = generate_nonce()
    params = {
        "utm_source": "miniprogram",
        "utm_medium": "wechatapp",
        "client_time": CURRENT_TIME,
        "sign_key": sign_info['set_time'],
        "device_id": sign_info['set_device_id'],
        "app_version": "3.0.9",
        "latitude": "0",
        "longitude": "0",
        "noncestr": nonce,
        "access_token": api_access_token,
        "login_token": login_token,
        "city_id": "0",
        "city_name": "0",
    }
    pprint.pprint(params)
    api_sign = generate_api_sign(params, url, sign_info['api_key'])
    print(f"api_sign: {api_sign}")
    params['api_sign'] = api_sign

    headers = {
        "Host": "xapi.quyundong.com",
        "systeminfo": "{\"model\":\"MacBookPro18,1\",\"system\":\"Mac OS X 14.5.0\",\"version\":\"3.8.8\","
                      "\"brand\":\"apple\",\"platform\":\"mac\",\"pixelRatio\":2,\"windowWidth\":414,\""
                      "windowHeight\":736,\"language\":\"zh_CN\",\"screenWidth\":414,\"screenHeight\":736,\""
                      "SDKVersion\":\"3.3.5\",\"fontSizeSetting\":15,\"statusBarHeight\":0}",
        "xweb_xhr": "1",
        "env-tag": "feature/v405",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) "
                      "NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.get(url, headers=headers, params=params, verify=False, proxies={"https": PROXY}, timeout=5)
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("status") == "0000":
            return response_json['data']['value']
        else:
            raise Exception(response.text)
    else:
        raise Exception(response.text)


def get_api_access_token(sign_info: dict):
    """
    获取业务接口的token
    """
    url = "https://xapi.quyundong.com/Api/User/getAccessToken"
    params = {
        "utm_source": "miniprogram",
        "utm_medium": "wechatapp",
        "client_time": CURRENT_TIME,
        "sign_key": sign_info['set_time'],
        "device_id": sign_info['set_device_id'],
        "app_version": "3.0.9",
        "latitude": "0",
        "longitude": "0",
        "noncestr": nonce,
        "access_token": "",
        "login_token": "",
        "city_id": "0",
        "city_name": "0"
    }
    api_sign = generate_api_sign(params, url, sign_info['api_key'])
    print(f"api_sign: {api_sign}")
    params['api_sign'] = api_sign

    headers = {
        "Host": "xapi.quyundong.com",
        "systeminfo": "{\"model\":\"MacBookPro18,1\",\"system\":\"Mac OS X 14.5.0\",\"version\":\"3.8.8\","
                      "\"brand\":\"apple\",\"platform\":\"mac\",\"pixelRatio\":2,\"windowWidth\":414,\""
                      "windowHeight\":736,\"language\":\"zh_CN\",\"screenWidth\":414,\"screenHeight\":736,\""
                      "SDKVersion\":\"3.3.5\",\"fontSizeSetting\":15,\"statusBarHeight\":0}",
        "xweb_xhr": "1",
        "env-tag": "feature/v405",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) "
                      "NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.get(url, headers=headers, params=params, verify=False, proxies={"https": PROXY}, timeout=5)
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("status") == "0000":
            return response_json["data"]['token']
        else:
            raise Exception(response.text)
    else:
        raise Exception(response.text)


def get_api_sign_from_serverless(sign_info: dict, serverless_token: str, api_access_token: str, login_token: str,
                                 date: str):
    """
    从云函数获取签名
    """
    url = "https://api.next.bspapp.com/client"
    data = {
        "method": "serverless.function.runtime.invoke",
        "params": json.dumps({
            "functionTarget": "uni-cloud-request",
            "functionArgs": {
                "api_key": sign_info['api_key'],
                "interfaceStr": "api:venues:booktable",
                "data": {
                    "utm_source": "miniprogram",
                    "utm_medium": "wechatapp",
                    "client_time": CURRENT_TIME,
                    "sign_key": sign_info['set_time'],
                    "device_id": sign_info['set_device_id'],
                    "app_version": "3.0.9",
                    "latitude": "22.53092098",
                    "longitude": "113.94631578",
                    "noncestr": nonce,
                    "access_token": api_access_token,
                    "login_token": login_token,
                    "city_id": 321,
                    "city_name": "上海",
                    "ver": "2.9",
                    "venues_id": "22377",
                    "cat_id": "12",
                    "book_date": date,
                    "raise_package_id": 0,
                    "phone_encode": "ks/Whad3C1TXSmRMAqxKvw=="
                },
                "clientInfo": {
                    "PLATFORM": "mp-weixin",
                    "OS": "mac",
                    "APPID": "__UNI__902073B",
                    "DEVICEID": sign_info['set_device_id'],
                    "scene": 1089,
                    "albumAuthorized": True,
                    "benchmarkLevel": -1,
                    "bluetoothEnabled": False,
                    "cameraAuthorized": True,
                    "locationAuthorized": True,
                    "locationEnabled": True,
                    "microphoneAuthorized": True,
                    "notificationAuthorized": True,
                    "notificationSoundEnabled": True,
                    "power": 100,
                    "safeArea": {
                        "bottom": 736,
                        "height": 736,
                        "left": 0,
                        "right": 414,
                        "top": 0,
                        "width": 414
                    },
                    "screenHeight": 736,
                    "screenWidth": 414,
                    "statusBarHeight": 0,
                    "theme": "light",
                    "wifiEnabled": True,
                    "windowHeight": 736,
                    "windowWidth": 414,
                    "enableDebug": False,
                    "devicePixelRatio": 2,
                    "deviceId": sign_info['set_device_id'],
                    "safeAreaInsets": {
                        "top": 0,
                        "left": 0,
                        "right": 0,
                        "bottom": 0
                    },
                    "appId": "__UNI__902073B",
                    "appName": "趣运动(新)",
                    "appVersion": "1.0.0",
                    "appVersionCode": "100",
                    "appLanguage": "zh-Hans",
                    "uniCompileVersion": "3.99",
                    "uniRuntimeVersion": "3.99",
                    "uniPlatform": "mp-weixin",
                    "deviceBrand": "apple",
                    "deviceModel": "MacBookPro18,1",
                    "deviceType": "pc",
                    "osName": "mac",
                    "osVersion": "OS",
                    "hostTheme": "light",
                    "hostVersion": "3.8.8",
                    "hostLanguage": "zh-CN",
                    "hostName": "WeChat",
                    "hostSDKVersion": "3.3.5",
                    "hostFontSizeSetting": 15,
                    "windowTop": 0,
                    "windowBottom": 0,
                    "locale": "zh-Hans",
                    "LOCALE": "zh-Hans"
                }
            }
        }),
        "spaceId": SERVERLESS_SPACE_ID,
        "timestamp": CURRENT_TIME,
        "token": serverless_token
    }
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # pprint.pprint(data)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    serverless_sign = Ae(data, SERVERLESS_CLIENT_SECRET)

    headers = {
        "Host": "api.next.bspapp.com",
        "x-basement-token": serverless_token,
        "xweb_xhr": "1",
        "x-serverless-sign": serverless_sign,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) "
                      "NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, proxies={"https": PROXY},
                                 timeout=5)
    else:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("success"):
            return response_json
        else:
            raise Exception(response.text)
    else:
        raise Exception(response.text)


def get_tennis_court_data(sign_info: dict, api_access_token: str, login_token: str, serverless_api_sign_info: dict,
                          date: str, is_retry: bool = False):
    """
    查询场地数据
    """
    print(f"sign_info: {sign_info}")
    print(f"api_access_token: {api_access_token}")
    print(f"login_token: {login_token}")
    print(f"serverless_api_sign_info: {serverless_api_sign_info}")
    print(f"nonce: {nonce}")

    url = "https://xapi.quyundong.com/Api/Venues/bookTable"
    headers = {
        "Host": "xapi.quyundong.com",
        "systeminfo": "{\"model\":\"MacBookPro18,1\",\"system\":\"Mac OS X 14.5.0\",\"version\":\"3.8.8\",\"brand"
                      "\":\"apple\",\"platform\":\"mac\",\"pixelRatio\":2,\"windowWidth\":414,\"windowHeight\":736,"
                      "\"language\":\"zh_CN\",\"screenWidth\":414,\"screenHeight\":736,\"SDKVersion\":\"3.3.5\","
                      "\"fontSizeSetting\":15,\"statusBarHeight\":0}",
        "xweb_xhr": "1",
        "env-tag": "feature/v405",
        "unicloudrequestid": serverless_api_sign_info['header']['x-serverless-request-id'],
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) "
                      "NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080812) XWEB/1216",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://servicewechat.com/wxbb9c3b35727d8ce8/149/page-frame.html",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    params = {
                "utm_source": "miniprogram",
                "utm_medium": "wechatapp",
                "client_time": CURRENT_TIME,
                "sign_key": sign_info['set_time'],
                "device_id": sign_info['set_device_id'],
                "app_version": "3.0.9",
                "latitude": "22.53092098",
                "longitude": "113.94631578",
                "noncestr": nonce,
                "access_token": api_access_token,
                "login_token": login_token,
                "city_id": 321,
                "city_name": "上海",
                "ver": "2.9",
                "venues_id": "22377",
                "cat_id": "12",
                "book_date": date,
                "raise_package_id": 0,
                "phone_encode": "ks/Whad3C1TXSmRMAqxKvw=="
    }
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # pprint.pprint(params)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    api_sign = generate_api_sign(params, url, sign_info['api_key'])
    print(f"api_sign: {api_sign}")
    params['api_sign'] = serverless_api_sign_info['data']

    print(url)
    if PROXY:
        print(f"PROXY: {PROXY}")
        response = requests.get(url, headers=headers, params=params, verify=False, proxies={"https": PROXY}, timeout=5)
    else:
        response = requests.get(url, headers=headers, params=params, verify=False)
    print(response.text)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("status") == "0000":
            return response_json['data']
        elif response_json.get('msg') == "AccessToken已失效(1)" and not is_retry:
            api_access_token = load_api_access_token(using_cached=False)
            serverless_token = load_serverless_token(using_cached=False)
            api_sign_info = get_api_sign_from_serverless(sign_info, serverless_token, api_access_token, login_token,
                                                         date)
            data = get_tennis_court_data(sign_info, api_access_token, login_token, api_sign_info, date, is_retry=True)
            return data
        else:
            raise Exception(response.text)
    else:
        raise Exception(response.text)


def get_proxy_list() -> list:
    """
    获取代理列表
    """
    # 获取公网HTTPS代理列表
    url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt"
    response = requests.get(url, verify=False)
    text = response.text.strip()
    lines = text.split("\n")
    proxy_list = [line.strip() for line in lines]
    random.shuffle(proxy_list)  # 每次都打乱下
    print(f"Loaded {len(proxy_list)} proxies from {url}")
    return proxy_list


def get_tennis_court_data_by_proxy(date: str, last_proxy: str = None):
    """
    通过代理查询场地数据
    """
    global PROXY
    proxy_list = get_proxy_list()
    if last_proxy:
        proxy_list.insert(0, last_proxy)
    else:
        pass
    for proxy in proxy_list:
        print(f"try proxy {proxy}....")
        PROXY = proxy
        try:
            sign_info = load_sign_info(using_cached=True)
            access_token = load_serverless_token(using_cached=True)
            api_access_token = load_api_access_token(using_cached=True)
            login_token = load_login_token(using_cached=True)

            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"sign_info: {sign_info}")
            print(f"access_token: {access_token}")
            print(f"api_access_token: {api_access_token}")
            print(f"login_token: {login_token}")
            print(f"sign_info: {sign_info}")
            api_sign_info = get_api_sign_from_serverless(sign_info, access_token, api_access_token, login_token, date)
            data = get_tennis_court_data(sign_info, api_access_token, login_token, api_sign_info, date)
            print(f"data: {data}")
            print(f"[success]: {PROXY}")

            court_free_time_infos = {}
            for good in data['goods_list']:
                court_name = good['course_name']
                free_time_slot_list = []
                for item in good['items']:
                    item_list = str(item).split(',')
                    status = item_list[3]
                    start_time = item_list[1]
                    end_time = item_list[8]
                    if len(start_time) == 4:
                        start_time = "0" + start_time
                    if len(end_time) == 4:
                        end_time = "0" + end_time
                    if status == '0':
                        free_time_slot_list.append([start_time, end_time])
                    else:
                        pass
                if free_time_slot_list:
                    court_free_time_infos[court_name] = free_time_slot_list
                else:
                    pass
            return court_free_time_infos, proxy
        except Exception as error:
            print(f"[fail]: {PROXY}, {str(error)}")
            continue
    raise Exception(f"all proxy failed!")


def send_sms_for_news(phone_num_list: list, param_list: list, template_id: str = '1856675'):
    """
    发生短信通知
    example: send_sms_for_news(["xxxxx"], param_list=["08-03", "大沙河", "21:00", "20:00"])
    """
    secret_id = os.environ.get("TENCENT_CLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENT_CLOUD_SECRET_KEY")
    sign_name = "网球场预定助手小程序"
    try:
        # 必要步骤：
        # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
        # 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
        # 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
        # 以免泄露密钥对危及你的财产安全。
        # SecretId、SecretKey 查询: https://console.cloud.tencent.com/cam/capi
        cred = credential.Credential(secret_id, secret_key)
        # cred = credential.Credential(
        #     os.environ.get(""),
        #     os.environ.get("")
        # )

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        # 如果需要指定proxy访问接口，可以按照如下方式初始化hp（无需要直接忽略）
        # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        # 实例化要请求产品(以sms为例)的client对象
        # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，支持的地域列表参考
        # https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
        # 属性可能是基本类型，也可能引用了另一个数据结构
        # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
        req = models.SendSmsRequest()

        # 基本类型的设置:
        # SDK采用的是指针风格指定参数，即使对于基本类型你也需要用指针来对参数赋值。
        # SDK提供对基本类型的指针引用封装函数
        # 帮助链接：
        # 短信控制台: https://console.cloud.tencent.com/smsv2
        # 腾讯云短信小助手: https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81

        # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
        # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
        req.SmsSdkAppId = "1400835675"
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
        # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
        req.SignName = sign_name
        # 模板 ID: 必须填写已审核通过的模板 ID
        # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
        req.TemplateId = template_id
        # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
        req.TemplateParamSet = param_list
        # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = phone_num_list
        # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = ""
        # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.ExtendCode = ""
        # 国内短信无需填写该项；国际/港澳台短信已申请独立 SenderId 需要填写该字段，默认使用公共 SenderId，无需填写该字段。
        # 注：月度使用量达到指定量级可申请独立 SenderId 使用，详情请联系
        # [腾讯云短信小助手](https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81)。
        req.SenderId = ""

        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)


def print_with_timestamp(*args, **kwargs):
    """
    打印函数带上当前时间戳
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print(timestamp, *args, **kwargs)


def merge_time_ranges(data: List[List[str]]) -> List[List[str]]:
    """
    将时间段合并
    Args:
        data: 包含多个时间段的列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '08:00'], ['07:00', '09:00'], ...]
    Returns:
        合并后的时间段列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '09:00'], ['09:00', '16:00'], ...]
    """
    if not data:
        return data
    else:
        pass
    print(f"merging {data}")
    # 将时间段转换为分钟数，并按照开始时间排序
    data_in_minutes = sorted([(int(start[:2]) * 60 + int(start[3:]), int(end[:2]) * 60 + int(end[3:]))
                              for start, end in data])

    # 合并重叠的时间段
    merged_data = []
    start, end = data_in_minutes[0]
    for i in range(1, len(data_in_minutes)):
        next_start, next_end = data_in_minutes[i]
        if next_start <= end:
            end = max(end, next_end)
        else:
            merged_data.append((start, end))
            start, end = next_start, next_end
    merged_data.append((start, end))

    # 将分钟数转换为时间段
    result = [[f'{start // 60:02d}:{start % 60:02d}', f'{end // 60:02d}:{end % 60:02d}'] for start, end in merged_data]
    print(f"merged {result}")
    return result


# TESTING
if __name__ == '__main__':
    """
    云函数入口
    :param event:
    :param context:
    :return:
    """
    if datetime.time(0, 0) <= datetime.datetime.now().time() < datetime.time(8, 0):
        print("每天0点-8点不巡检")
        exit()
    else:
        pass

    # 获取脚本运行的时间
    start_min_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    end_min_time = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:00")

    # 网球场守望者开始时间
    run_start_time = time.time()
    print_with_timestamp("start to check...")

    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--phone', type=int, help='phone num', required=False)
    # 解析命令行参数
    args = parser.parse_args()
    # 检查必需的参数是否输入
    if not all([args.phone]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.phone)

    # 查询空闲的球场信息
    up_for_send_data_list = []
    success_proxy = None
    for index in range(0, 7):
        input_date = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        inform_date = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%m-%d')
        court_data, success_proxy = get_tennis_court_data_by_proxy(input_date, success_proxy)
        time.sleep(1)
        if court_data:
            free_slot_list = []
            for court_name, free_time_slot_list in court_data.items():
                for time_slot in free_time_slot_list:
                    print(time_slot)
                    hour_num = int(time_slot[0].split(':')[0])
                    if 8 <= hour_num <= 21:
                        free_slot_list.append(time_slot)
                    else:
                        pass
            if free_slot_list:
                merged_free_slot_list = merge_time_ranges(free_slot_list)
                up_for_send_data_list.append({"date": inform_date,
                                              "court_name": "青少体育",
                                              "free_slot_list": merged_free_slot_list})
            else:
                pass
        else:
            pass
    print(f"up_for_send_data_list: {up_for_send_data_list}")
    up_for_send_sms_list = []
    if up_for_send_data_list:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信
        # 获取当前脚本的名称
        script_name = os.path.basename(__file__)
        cache = shelve.open(f'./{script_name}_cache')
        for up_for_send_data in up_for_send_data_list:
            date = up_for_send_data['date']
            court_name = up_for_send_data['court_name']
            free_slot_list = up_for_send_data['free_slot_list']
            for free_slot in free_slot_list:
                cache_key = f"{court_name}_{date}_{free_slot[0]}"
                if cache_key in cache:
                    # 已通知过
                    print(f"已通知: {up_for_send_data}")
                    pass
                else:
                    # 加入待发送短信队里
                    print(f"准备通知: {up_for_send_data}")
                    up_for_send_sms_list.append({"phone": str(args.phone),
                                                 "date": date,
                                                 "court_name": court_name,
                                                 "start_time": free_slot[0],
                                                 "end_time": free_slot[1],
                                                 })
                    # 更新本地文件缓存
                    cache[cache_key] = 1
        # 关闭本地文件缓存
        cache.close()

        if up_for_send_data_list:
            # 发送短信
            for sms_info in up_for_send_sms_list:
                print(f"sending {sms_info}...")
                phone = sms_info['phone']
                date = sms_info['date']
                court_name = sms_info['court_name']
                start_time = sms_info['start_time']
                end_time = sms_info['end_time']
                sms_res = send_sms_for_news([phone], [date, court_name, start_time, end_time])
                print(sms_res)
                if "send success" in str(sms_res):
                    print_with_timestamp("短信发送成功")
                else:
                    print_with_timestamp("短信发送失败")
                time.sleep(5)
        else:
            print("无需要发送的短信")
    else:
        print_with_timestamp(F"无需要通知的场地信息")

    # 计算整体运行耗时
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print_with_timestamp(f"Total cost time：{execution_time} s")

    # 缓存记录到日志
    if up_for_send_data_list or up_for_send_sms_list:
        status = 1
    else:
        status = 0
    output_data = {"start_time": start_min_time, "end_time": end_min_time,
                   "status": status, "place_name": "青少体育", "city": "上海",
                   "up_for_send_num": len(up_for_send_data_list), "send_num": len(up_for_send_sms_list)}
    print(F"[GRAFANA_DATA]@{json.dumps(output_data)}")
