#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/10 21:41
@Author  : claude89757
@File    : common.py
@Software: PyCharm
"""
import os
import requests
import time
import math
import random
import json
import hashlib
import datetime
import calendar

from typing import List
from config import COURT_NAME_INFOS

# 读取指定环境变量的值
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SIGN_KEY = os.environ.get("SIGN_KEY")
KS_TOKEN = os.environ.get("KS_TOKEN")  # 酷尚网球的token可能会过期...


def gen_nonce(timestamp: int):
    """
    生成 nonce, 该方法解析自前端 js 代码, 大概率不会变化
    """
    e = int(timestamp)
    y = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    nonce = ''
    for c in y:
        n = math.trunc((e + 16 * random.random()) % 16)
        e = math.floor(e / 16)
        if 'x' == c:
            nonce += hex(n)[2]
        elif 'y' == c:
            nonce += hex(3 & n | 8)[2]
        else:
            nonce += c
    return nonce


def signature_for_post(timestamp: str, nonce: str, param: str = '', data: dict = None):
    """
    生成post请求的签名
    """
    prefix = '&'.join(
        [f'_key={SIGN_KEY}', '_timestamp=' + timestamp, '_nonce=' + nonce])
    prefix += ',,' + param + ',,'
    if data is not None:
        raw = prefix + json.dumps(data, separators=(',', ':'))
    else:
        raw = prefix
    return hashlib.md5(raw.encode()).hexdigest().upper()


def signature_for_get(timestamp: str, nonce: str, param_str: str = ''):
    """
    生成get请求的签名
    """
    prefix = ','.join([
         f'_key={SIGN_KEY}&_timestamp={timestamp}&_nonce={nonce}',
         param_str,
         "",
         "",
         ""
    ])
    print(prefix)
    return hashlib.md5(prefix.encode()).hexdigest().upper()


def clock_to_timestamp(hour: str):
    """
    福田体育的时间戳比较特殊 (奇葩), 它其实是以 2013-01-01 {hour}:00 为基准, 计算出新的时间戳
    其中 hour 为预订时间
    """
    return int(
        datetime.datetime.strptime(f'2013-01-01 {hour}:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)


def timestamp_to_clock(timestamp: int) -> str:
    """
    timestamp 为 Unix 时间戳（毫秒）
    返回值为时钟格式（小时:分钟）
    """
    date = datetime.datetime.fromtimestamp(timestamp / 1000)  # 将毫秒转换为秒
    return date.strftime('%H:%M')


def str_to_timestamp(date_str: str):
    return int(datetime.datetime.strptime(date_str, '%Y-%m-%d').timestamp() * 1000)


def find_available_slots(booked_slots, time_range):
    """
    根据已预定的时间段，查询可预定的时间段
    """
    print(f"input: {booked_slots}")
    print(f"time_range: {time_range}")
    for slot in booked_slots:
        for index in range(len(slot)):
            if slot[index] == '00:00':
                slot[index] = "23:59"
            else:
                pass
    booked_slots = sorted(booked_slots, key=lambda x: x[0])  # 按开始时间排序
    available_slots = []

    current_time = datetime.datetime.strptime(time_range['start_time'], "%H:%M")
    end_time = datetime.datetime.strptime(time_range['end_time'], "%H:%M")

    for slot in booked_slots:
        slot_start = datetime.datetime.strptime(slot[0], "%H:%M")
        slot_end = datetime.datetime.strptime(slot[1], "%H:%M")

        if current_time < slot_start:
            available_slots.append([current_time.strftime("%H:%M"), slot_start.strftime("%H:%M")])

        # 如果当前时间小于已预定时间段的结束时间，更新当前时间为已预定时间段的结束时间
        if current_time < slot_end:
            current_time = slot_end

    if current_time < end_time:
        available_slots.append([current_time.strftime("%H:%M"), end_time.strftime("%H:%M")])
    print(f"output: {available_slots}")
    return available_slots


def get_free_tennis_court_infos_for_isz(date: str, proxy_list: list, time_range: dict,
                                        sales_item_id: str, sales_id: str) -> dict:
    """
    获取可预订的场地信息
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        check_data = str_to_timestamp(date)
        timestamp = math.trunc(time.time() * 1000)
        nonce = gen_nonce(timestamp)
        params = {
            "salesItemId": sales_item_id,
            "curDate": str(check_data),
            "venueGroupId": "",
            "_time": str(timestamp)
        }
        param_str = f"salesItemId={sales_item_id}&curDate={check_data}&venueGroupId=&_time={str(timestamp)}"  # 仅用于签名
        signature = signature_for_get(str(timestamp), nonce.replace('-', ''), param_str=param_str)
        headers = {
            "Host": "isz.ydmap.cn",
            "accept": "application/json, text/plain, */*",
            "openid-token": "",
            "nonce": nonce.replace('-', ''),
            "timestamp": str(timestamp),
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "accept-language": "zh-CN,zh-Hans;q=0.9",
            "entry-tag": "",
            "signature": signature,
            "sec-fetch-mode": "cors",
            # "access-token": access_token,  # get请求不需要
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 "
                          "(KHTML, like Gecko) "
                          "Mobile/15E148/openweb=paschybrid/SZSMT_IOS,VERSION:4.5.0",
            "referer": F"https://isz.ydmap.cn/booking/schedule/{sales_id}?salesItemId={sales_item_id}",
            "sec-fetch-dest": "empty"
        }
        url = "https://isz.ydmap.cn/srv100352/api/pub/sport/venue/getVenueOrderList"
        print(url)
        print(params)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    now = datetime.datetime.now().time()
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    if got_response:
        if response.status_code == 200:
            if response.json()['code'] == 0:
                booked_court_infos = {}
                for data in response.json()['data']:
                    start_time = timestamp_to_clock(data['startTime'])
                    end_time = timestamp_to_clock(data['endTime'])
                    if booked_court_infos.get(data['venueId']):
                        booked_court_infos[data['venueId']].append([start_time, end_time])
                    else:
                        booked_court_infos[data['venueId']] = [[start_time, end_time]]
                available_slots_infos = {}
                for venue_id, booked_slots in booked_court_infos.items():
                    if venue_id in [104300, 104301, 104302, 104475]:
                        # 黄木岗的训练墙剔除
                        continue
                    elif venue_id == 102930:
                        if date != today_str:
                            # 香蜜6号场，非当日的场地信息过滤
                            continue
                        else:
                            pass
                    else:
                        pass
                    available_slots = find_available_slots(booked_slots, time_range)
                    available_slots_infos[venue_id] = available_slots
                filter_available_slots_infos = {}
                for venue_id, available_slots in available_slots_infos.items():
                    if venue_id == 102930 and (available_slots == [['08:00', '22:30']]
                                               or available_slots == [['09:00', '22:30']]
                                               or available_slots == [['10:00', '22:30']]):
                        pass
                    else:
                        filter_available_slots_infos[venue_id] = available_slots
                return filter_available_slots_infos
            else:
                raise Exception(response.text)
        else:
            raise Exception(response.text)
    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_zjclub(date: str, proxy_list: list, time_range: dict,
                                           sales_item_id: str = "100586", sales_id: str = "102042") -> dict:
    """
    获取可预订的场地信息
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        check_data = str_to_timestamp(date)
        timestamp = math.trunc(time.time() * 1000)
        nonce = gen_nonce(timestamp)
        params = {
            "salesItemId": sales_item_id,
            "curDate": str(check_data),
            "venueGroupId": "",
            "_time": str(timestamp)
        }
        param_str = f"salesItemId={sales_item_id}&curDate={check_data}&venueGroupId=&_time={str(timestamp)}"  # 仅用于签名
        signature = signature_for_get(str(timestamp), nonce.replace('-', ''), param_str=param_str)
        headers = {
            "Host": "isz.ydmap.cn",
            "accept": "application/json, text/plain, */*",
            "openid-token": "",
            "nonce": nonce.replace('-', ''),
            "timestamp": str(timestamp),
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "accept-language": "zh-CN,zh-Hans;q=0.9",
            "entry-tag": "",
            "signature": signature,
            "sec-fetch-mode": "cors",
            # "access-token": access_token,  # get请求不需要
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 "
                          "(KHTML, like Gecko) "
                          "Mobile/15E148/openweb=paschybrid/SZSMT_IOS,VERSION:4.5.0",
            "referer": F"https://isz.ydmap.cn/booking/schedule/{sales_id}?salesItemId={sales_item_id}",
            "sec-fetch-dest": "empty"
        }
        url = "https://zjclub.ydmap.cn/srv100292/api/pub/sport/venue/getVenueOrderList"
        print(url)
        print(params)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    print(f"response: {response.text}")
    if got_response:
        if response.status_code == 200:
            if response.json()['code'] == 0:
                booked_court_infos = {}
                for data in response.json()['data']:
                    start_time = timestamp_to_clock(data['startTime'])
                    end_time = timestamp_to_clock(data['endTime'])
                    if booked_court_infos.get(data['venueId']):
                        booked_court_infos[data['venueId']].append([start_time, end_time])
                    else:
                        booked_court_infos[data['venueId']] = [[start_time, end_time]]
                available_slots_infos = {}
                for venue_id, booked_slots in booked_court_infos.items():
                    if venue_id in [104300, 104301, 104302, 104475]:
                        # 黄木岗的训练墙剔除
                        continue
                    elif venue_id in [102930]:
                        # 香蜜6号当日线下预定，剔除
                        continue
                    else:
                        pass
                    available_slots = find_available_slots(booked_slots, time_range)
                    available_slots_infos[venue_id] = available_slots
                return available_slots_infos
            else:
                raise Exception(response.text)
        else:
            raise Exception(response.text)
    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_hjd(date: str, proxy_list: list) -> dict:
    """
    从弘金地获取可预订的场地信息,
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        params = {
            "gymId": "1479063349546192897",
            "sportsType": "1",
            "reserveDate": date
        }
        headers = {
            "Host": "gateway.gemdalesports.com",
            "referer": "https://servicewechat.com/wxf7ae96551d92f600/34/page-frame.html",
            "xweb_xhr": "1",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/"
                          "98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000)"
                          " NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        url = "https://gateway.gemdalesports.com/inside-frontend/api/field/fieldReserve"
        print(url)
        print(params)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.get(url, headers=headers, params=params, proxies=proxies, verify=False, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    if got_response:
        if response.json()['data'].get('array'):
            available_slots_infos = {}
            for file_info in response.json()['data']['array']:
                available_slots = []
                for slot in file_info['daySource']:
                    if slot['occupy']:
                        # 将字符串转换为时间对象
                        time_obj = datetime.datetime.strptime(slot['startTime'], "%H:%M")
                        # 将时间对象加上一小时
                        new_time_obj = time_obj + datetime.timedelta(hours=1)
                        # 将时间对象转换为字符串
                        end_time_str = new_time_obj.strftime("%H:%M")
                        available_slots.append([slot['startTime'], end_time_str])
                    else:
                        pass
                available_slots_infos[file_info['fieldName']] = merge_time_ranges(available_slots)
            return available_slots_infos
        else:
            raise Exception(response.text)

    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_tns(date: str, proxy_list: list) -> dict:
    """
    从弘金地获取可预订的场地信息,
    """
    # 时间段的映射表
    slot_map = {
        0: ['07:00', '07:30'],
        1: ['07:30', '08:00'],
        2: ['08:00', '08:30'],
        3: ['08:30', '09:00'],
        4: ['09:00', '09:30'],
        5: ['09:30', '10:00'],
        6: ['10:00', '10:30'],
        7: ['10:30', '11:00'],
        8: ['11:00', '11:30'],
        9: ['11:30', '12:00'],
        10: ['12:00', '12:30'],
        11: ['12:30', '13:00'],
        12: ['13:00', '13:30'],
        13: ['13:30', '14:00'],
        14: ['14:00', '14:30'],
        15: ['14:30', '15:00'],
        16: ['15:00', '15:30'],
        17: ['15:30', '16:00'],
        18: ['16:00', '16:30'],
        19: ['16:30', '17:00'],
        20: ['17:00', '17:30'],
        21: ['17:30', '18:00'],
        22: ['18:00', '18:30'],
        23: ['18:30', '19:00'],
        24: ['19:00', '19:30'],
        25: ['19:30', '20:00'],
        26: ['20:00', '20:30'],
        27: ['20:30', '21:00'],
        28: ['21:00', '21:30'],
        29: ['21:30', '22:00'],
        30: ['22:00', '22:30'],
        31: ['22:30', '23:00'],
        32: ['23:00', '23:30'],
        33: ['23:30', '00:00']
    }
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        payload = {
            "id": "3203",
            "time": date
        }
        headers = {
            "Host": "chaapi.dzxwbj.com",
            "xweb_xhr": "1",
            "referer": "https://servicewechat.com/wx337fddd4f7149756/3/page-frame.html",
            "adminid": "633",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI"
                          " MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
            "content-type": "application/json",
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-language": "zh-CN,zh",
        }
        url = "https://chaapi.dzxwbj.com/Chang/timeListchang"
        print(url)
        print(payload)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies,
                                     verify=False, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    if got_response:
        if response.json()['data'].get('store'):
            available_slots_infos = {}
            for file_info in response.json()['data']['store']:
                if "单打" in file_info['name']:
                    continue
                else:
                    pass
                available_slots = []
                for index in range(len(file_info['list'])):
                    slot_info = file_info['list'][index]
                    slot = slot_map[index]
                    if slot_info['status'] == 0:
                        available_slots.append(slot)
                    else:
                        pass
                available_slots_infos[file_info['name']] = merge_time_ranges(available_slots)
            return available_slots_infos
        else:
            raise Exception(response.text)

    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_ks(date: str, proxy_list: list) -> dict:
    """
    从弘金地获取可预订的场地信息,
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        data = {
            "date": date,
            "token": KS_TOKEN,
            "tempStoreId": "10",
            "companyId": ""
        }
        headers = {
            "Host": "api.suncoolsports.com",
            "referer": "https://servicewechat.com/wx702009499d3e30ec/20/page-frame.html",
            "xweb_xhr": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI "
                          "MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
            "form-type": "routine",
            "content-type": "application/json",
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-language": "zh-CN,zh",
        }
        url = "https://api.suncoolsports.com/u-spacelist"
        print(url)
        print(data)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies,
                                     verify=False, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    if got_response:
        if response.json()['data'].get('children'):
            available_slots_infos = {}
            for file_info in response.json()['data']['children']:
                start_time = str(file_info['time']).split('~')[0]
                end_time = str(file_info['time']).split('~')[1]
                for data in file_info['children']:
                    if data['active'] == 1:
                        if available_slots_infos.get(data['name']):
                            available_slots_infos[data['name']].append([start_time, end_time])
                        else:
                            available_slots_infos[data['name']] = [[start_time, end_time]]
                    else:
                        pass
            # 合并时间段
            merged_available_slots_infos = {}
            for item_name, slot_list in available_slots_infos.items():
                merged_available_slots_infos[item_name] = merge_time_ranges(slot_list)
            return merged_available_slots_infos
        else:
            raise Exception(response.text)

    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_wcjt(date: str, proxy_list: list = None) -> dict:
    """
    从弘金地获取可预订的场地信息,
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        data = {
            "action": "GetSeatMap",
            "CardTypeId": "208",
            "ArenaId": "3",
            "DateTime": date,
            "IsPrivilege": "0"
        }
        headers = {
            "Host": "mlwtzxwx.x-saas.com",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) "
                          "MacWechat/3.8.1(0x13080110) XWEB/30626 Flue",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://mlwtzxwx.x-saas.com",
            "Referer": "http://mlwtzxwx.x-saas.com/Booking/ArenaBooking.aspx?ArenaId=3&IsSee=1",
            "Accept-Language": "zh-CN,zh",
        }
        url = "http://mlwtzxwx.x-saas.com/Booking/Booking.ashx?ajaxGuid=0720174245636"
        print(url)
        print(data)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            if proxy_list:
                response = requests.post(url, headers=headers, data=data, proxies=proxies,
                                         timeout=5)
            else:
                response = requests.post(url, headers=headers, data=data,
                                         timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    if got_response:
        if response.json().get('data'):
            available_slots_infos = {}
            for data in response.json()['data']:
                start_time = data['SchemeTime']
                time_obj = datetime.datetime.strptime(start_time, "%H:%M")  # 将字符串转换为datetime对象
                new_time_obj = time_obj + datetime.timedelta(hours=1)  # 将时间加一小时
                end_time = new_time_obj.strftime("%H:%M")  # 将datetime对象转换为字符串
                for seat in data['Seats']:
                    seat_name = seat['SeatName']
                    if seat['SeatStatus'] == 0:
                        if available_slots_infos.get(seat_name):
                            available_slots_infos[seat_name].append([start_time, end_time])
                        else:
                            available_slots_infos[seat_name] = [[start_time, end_time]]
                    else:
                        pass
            # 合并时间段
            merged_available_slots_infos = {}
            for item_name, slot_list in available_slots_infos.items():
                merged_available_slots_infos[item_name] = merge_time_ranges(slot_list)
            return merged_available_slots_infos
        else:
            raise Exception(response.text)

    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_dsports(date: str, proxy_list: list = None) -> dict:
    """
    从大生体育获取可预订的场地信息,
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        data = {
            "userid": "",
            "gcategoryid": "3",
            "site_id": "88",
            "site_name": "莲花二村网球场",
            "address": "深圳市福田区莲花二村",
            "cancel_tips": "退场规定：室内场地、室外场地（非天气原因）退场，须提前24小时，否则场馆将谢绝退场申请，谢谢支持。",
            "version": "8.0",
            "pre_date": date,
            "pre_type": "0"
        }
        headers = {
            "Host": "wap.dsports.co",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000)"
                          " MacWechat/3.8.1(0x13080110) XWEB/30626 Flue",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://wap.dsports.co",
            "Referer": "http://wap.dsports.co/Enrol/SingleVenue?%7B%22i%22:%2288%22,%22c%22:%223%22%7D=",
            "Accept-Language": "zh-CN,zh",
        }
        url = "http://wap.dsports.co/Site/GetPlayPreList"
        print(url)
        print(data)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            if proxy_list:
                response = requests.post(url, headers=headers, data=data, proxies=proxies,
                                         timeout=5)
            else:
                response = requests.post(url, headers=headers, data=data,
                                         timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    if got_response:
        if response.json().get('data'):
            available_slots_infos = {}
            for data in response.json()['data'][0]['ListPlayDetails']:
                seat_name = data['posi_name']

                for slot_info in data['ListPlayPreDet']:
                    time_str = slot_info['preId'][8:12]
                    start_time = f"{time_str[:2]}:{time_str[2:]}"  # 将时间格式化为 "HH:mm"
                    time_obj = datetime.datetime.strptime(start_time, "%H:%M")  # 将字符串转换为datetime对象
                    new_time_obj = time_obj + datetime.timedelta(hours=1)  # 将时间加一小时
                    end_time = new_time_obj.strftime("%H:%M")  # 将datetime对象转换为字符串
                    if slot_info['statusStr'] == "可约":
                        if available_slots_infos.get(seat_name):
                            available_slots_infos[seat_name].append([start_time, end_time])
                        else:
                            available_slots_infos[seat_name] = [[start_time, end_time]]
                    else:
                        pass
            # 合并时间段
            merged_available_slots_infos = {}
            for item_name, slot_list in available_slots_infos.items():
                merged_available_slots_infos[item_name] = merge_time_ranges(slot_list)
            return merged_available_slots_infos
        else:
            raise Exception(response.text)

    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_shanhua(date: str, proxy_list: list, time_range: dict) -> dict:
    """
    获取可预订的场地信息
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        data = {
            "kdtid": "92195500",
            "timeStart": f"{''.join(date.split('-'))}000000",
            "timeEnd": f"{''.join(date.split('-'))}235959",
            "serviceId": 9381755,
            "mode": 3
        }
        headers = {
            "Host": "book.isv.youzan.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/"
                          "WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626",
            "content-type": "application/json;charset=UTF-8",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://book.isv.youzan.com/pages/applet?kdtId=92195500&busId=3771871&source=1&sId=9381755",
            "accept-language": "zh-CN,zh",
        }
        url = "https://book.isv.youzan.com/api/v2/order/getListByStartedTime"
        print(url)
        print(data)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies,
                                     verify=False, timeout=5)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue
    print(f"response: {response}")
    # print(f"response: {response.text}")
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    if got_response:
        if response.status_code == 200:
            if response.json().get('message') == "成功":
                booked_court_infos = {}
                for data in response.json()['data']:
                    start_time = f"{str(data['orderStartedAt'])[8:10]}:{str(data['orderStartedAt'])[10:12]}"
                    end_time = f"{str(data['orderEndedAt'])[8:10]}:{str(data['orderEndedAt'])[10:12]}"  # 时间格式化
                    if booked_court_infos.get(data['spaceId']):
                        booked_court_infos[data['spaceId']].append([start_time, end_time])
                    else:
                        booked_court_infos[data['spaceId']] = [[start_time, end_time]]
                available_slots_infos = {}
                for space_id, booked_slots in booked_court_infos.items():
                    available_slots = find_available_slots(booked_slots, time_range)
                    available_slots_infos[space_id] = available_slots
                for space_id in [88371202, 88371216, 88371217, 88371218, 88371219, 88371220, 88371221, 88371222]:
                    if space_id not in available_slots_infos.keys():
                        available_slots_infos[space_id] = [["09:00", "22:00"]]
                return available_slots_infos
            else:
                raise Exception(response.text)
        else:
            raise Exception(response.text)
    else:
        raise Exception(f"all proxies failed")


def get_free_tennis_court_infos_for_szw(date: str, proxy_list: list, time_range: dict) -> dict:
    """
    获取可预订的场地信息
    """
    got_response = False
    response = None
    index_list = list(range(len(proxy_list)))
    # 打乱列表的顺序
    random.shuffle(index_list)
    print(index_list)
    for index in index_list:
        data = {
            'VenueTypeID': 'd3bc78ba-0d9c-4996-9ac5-5a792324decb',
            'VenueTypeDisplayName': '',
            # 'IsGetPrice': 'true',
            # 'isApp': 'true',
            'billDay': {date},
            # 'webApiUniqueID': '811e68e7-f189-675c-228d-3739e48e57b2'
        }
        headers = {
            'Host': 'program.springcocoon.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            # 'X-XSRF-TOKEN': 'WX8ov48Nfyv--FaZ5ugm6cbscc_'
            #                 'YOqfTVIr6Tobcku0Clt4Q4jtRZrg0YML14TNs6ukHgXsWyK_'
            #                 'OfgGvejxCaE7srNgpMwxjX9PUOU_JbIl3LkQx3aPI02YovKbqfUwOL5QMqw2',
            'Cookie': 'HT.ShopID.1=4f195d33-de51-495e-a345-09b23f98ce95;'
                      '.AspNet.ApplicationCookie=aQl5ju2OXLbnHuGbCI4T_8lLN_lwLDH22IgIMcjlzsNjRfvp'
                      'YYtYVSBcupIJ_2E2DHPkgYyme9MVWKVvbg97t-TrnYvtocP2BKipfpjl-ROPvdBwJ1BP0uWPpCMDIdSR7J7OdKqPHQ4'
                      '2Cj-A5ozeLS4_C7IYSjBHLUYwJm6rvq-5Sye187tT7GwmQJE5chg2U6mCL3X-EaRHf3cuk1En3Gyxjt-ZyPxmGZm_gP3'
                      'V1FWmMEEalM2gJH95BTTrEAQtAM3gTs1AURcwNmNQXiHSJzz79JTcKkTA3vYZamio4jkLGeQ_LnE5WQSm7x0QXFz3Sxi'
                      'vShX4EWvInkfm4hGqDUE_HlXL1eAR66WVh4TLWGXLUOolfz_F2fz9OE0vLyNvIBxsYdY_LqMbHyV5SbxxIOxgCgxM2aJ'
                      'Hw04WhY5S-8AOA5UVhWkNJwCWBcnk-6nNveQYNNWHJAICiLtlDJ7b6cbZ_8tlhnXcqvppcyJFLFOb1cl7yfPsn_uX69x'
                      'v-RU8neEP4pw-nuFkrbN8OGCeHTM2M8mA5dwxfdJ4lD92P3znT7T3b6cKeSuGxo-65HUKuTjCq_P3_qOMetN39CTDQn6E'
                      'ZY68uMF6OQzw3Nu1ge9ANTFM',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://program.springcocoon.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X)'
                          ' AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Mobile/15E148 MicroMessenger/8.0.39(0x18002733) '
                          'NetType/WIFI Language/zh_CN miniProgram/wx6b10d95e92283e1c',
            'Referer': 'https://program.springcocoon.com/szbay/AppVenue/VenueBill/'
                       'VenueBill?VenueTypeID=d3bc78ba-0d9c-4996-9ac5-5a792324decb',
            'Sec-Fetch-Dest': 'empty'
        }
        url = 'https://program.springcocoon.com/szbay/api/services/app/VenueBill/GetVenueBillDataAsync'
        print(url)
        print(data)
        # print(headers)
        proxy = proxy_list[index]
        print(f"trying for {index} time for {proxy}")
        try:
            proxies = {"https": proxy}
            response = requests.post(url, headers=headers, data=data, proxies=proxies, verify=False, timeout=30)
            # print(response.text)
            if response.status_code == 200:
                print(f"success for {proxy}")
                got_response = True
                time.sleep(1)
                break
            else:
                print(f"failed for {proxy}: {response}")
                continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"failed for {proxy}: {error}")
            continue

    if got_response:
        if response.status_code == 200:
            if len(response.json()['result']) == 1:
                # 场地名称转换
                venue_name_infos = {}
                for venue in response.json()['result'][0]['listVenue']:
                    venue_name_infos[venue['id']] = venue['displayName']
                print(venue_name_infos)

                booked_court_infos = {}
                for venue_info in response.json()['result'][0]['listWebVenueStatus']:
                    if venue_info['bookLinker'] == '可定' or venue_info['bookLinker'] == '可订':
                        pass
                    else:
                        start_time = str(venue_info['timeStartEndName']).split('-')[0].replace(":30", ":00")
                        end_time = str(venue_info['timeStartEndName']).split('-')[1].replace(":30", ":00")
                        venue_name = venue_name_infos[venue_info['venueID']]
                        if booked_court_infos.get(venue_name):
                            booked_court_infos[venue_name].append([start_time, end_time])
                        else:
                            booked_court_infos[venue_name] = [[start_time, end_time]]
                available_slots_infos = {}
                for venue_id, booked_slots in booked_court_infos.items():
                    available_slots = find_available_slots(booked_slots, time_range)
                    available_slots_infos[venue_id] = available_slots
                return available_slots_infos
            else:
                raise Exception(response.text)
        else:
            raise Exception(response.text)
    else:
        raise Exception(f"all proxies failed")


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


def sort_key(item):
    return int(item.split("号")[0])


def get_hit_court_infos(available_slice_infos: dict, rule_list: list) -> []:
    """
    查找出命中规则的时间段, 并打印详细的场地信息
    """
    # 推送可预定时间段的消息列表，并特别标注晚上时间段的场地
    msg_list = [f"网球场可预定时间段"]
    found_court_infos = []
    for date, free_slot_infos in available_slice_infos.items():
        # 检查是否有符合日期的推送规则
        filter_rule_list = []
        for rule in rule_list:
            check_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
            rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
            if rule_start_date <= check_date <= rule_end_date:
                # print(f"{date}在{rule['start_date']}和{rule['end_date']}之间")
                filter_rule_list.append(rule)
            else:
                # print(f"{date}不在{rule['start_date']}和{rule['end_date']}之间")
                pass

        weekday = calendar.day_name[datetime.datetime.strptime(date, '%Y-%m-%d').date().weekday()]
        weekday_cn = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四',
                      'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'}[weekday]
        date_and_weekday = f'{date}（{weekday_cn}）'
        msg_list.append(f"{date_and_weekday}")
        check_date_slot_list = []
        # print(F"free_slot_infos: {free_slot_infos}")
        # 检查是否有符合条件的时间段
        for court_name, slots in free_slot_infos.items():
            # print(f"slots: {slots}")
            # 将列表转换为元组，并将元组转换为集合，实现去重
            unique_data = set(tuple(item) for item in slots)
            # 将元组转换为列表，并按照第一个元素和第二个元素进行排序
            sorted_slot_list = sorted([list(item) for item in unique_data], key=lambda x: (x[0], x[1]))
            # print(f"sorted_slot_list: {sorted_slot_list}")
            # print(f"sorted_slot_list: {sorted_slot_list}")
            tag_slot_list = []
            for slot in sorted_slot_list:
                if not filter_rule_list:
                    # 无推送规则，无需进一步检查时间段
                    tag_slot_list.append(f"{slot[0]}-{slot[1]}")
                else:
                    # 有推送规则，详细继续检查时间段
                    cur_start_time = slot[0]
                    cur_end_time = slot[1]
                    hit_rule_list = []
                    for rule in filter_rule_list:
                        watch_start_time = rule['start_time']
                        watch_end_time = rule['end_time']
                        cur_start_time_obj = datetime.datetime.strptime(cur_start_time, "%H:%M")
                        cur_end_time_obj = datetime.datetime.strptime(cur_end_time, "%H:%M")
                        watch_start_time_obj = datetime.datetime.strptime(watch_start_time, "%H:%M")
                        watch_end_time_obj = datetime.datetime.strptime(watch_end_time, "%H:%M")
                        rule_duration = rule.get('duration', 2)
                        if not rule_duration:
                            rule_duration = 2
                        else:
                            pass
                        # 计算两个时间范围的交集
                        start_time = max(cur_start_time_obj, watch_start_time_obj)
                        end_time = min(cur_end_time_obj, watch_end_time_obj)
                        # 计算交集的时间长度
                        duration = end_time - start_time
                        if duration >= datetime.timedelta(hours=rule_duration):
                            # print("两个时间范围有交集，且交集的时间大于等于60分钟")
                            # 检查场地的结束时间比当前时间晚2小时以上
                            time_str = f"{date} {cur_end_time}"
                            time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                            if time_obj >= datetime.datetime.now() + datetime.timedelta(minutes=30):
                                # print(f"{time_str}比当前时间大于x小时, 来得及去打球")
                                hit_rule_list.append(rule)
                            else:
                                # print(f"{time_str}比当前时间小于等于x小时， 来不及去打球")
                                pass
                        else:
                            # print("两个时间范围没有交集，或者交集的时间小于60分钟")
                            pass
                    if hit_rule_list:
                        # 添加到待推送短信的列表中
                        for rule in hit_rule_list:
                            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                            formatted_date = date_obj.strftime('%m-%d')
                            found_court_infos.append({"rule_info": rule,
                                                      "_id": rule['_id'],
                                                      "phone": rule['phone'],
                                                      "date": f"{formatted_date} {weekday_cn}",
                                                      "court_index": COURT_NAME_INFOS.get(court_name, court_name),
                                                      "start_time": slot[0],
                                                      "end_time": slot[1]})

                        tag_slot_list.append(f"`{slot[0]}`-`{slot[1]}`")
                    else:
                        tag_slot_list.append(f"{slot[0]}-{slot[1]}")
            if tag_slot_list:
                check_date_slot_list.append(f"{court_name}: {'|'.join(tag_slot_list)}")
            else:
                pass
        if check_date_slot_list:
            sorted_check_date_slot_list = sorted(check_date_slot_list)
            check_date_slot_msg = "\n".join(sorted_check_date_slot_list)
            msg_list.append(f"{check_date_slot_msg}")
        else:
            msg_list.append(f"> 无场")
        msg_list.append("")
    msg = "\n".join(msg_list)
    print("打印场地的可预订信息============================================")
    print(msg)
    print("============================================")
    return found_court_infos


def print_with_timestamp(*args, **kwargs):
    """
    打印函数带上当前时间戳
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print(timestamp, *args, **kwargs)
