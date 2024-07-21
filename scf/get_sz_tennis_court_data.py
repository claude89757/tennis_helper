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


# 读取指定环境变量的值
SIGN_KEY = os.environ.get("SIGN_KEY")
SALES_ID = os.environ.get("SALES_ID")
SALES_ITEM_ID = os.environ.get("SALES_ITEM_ID")


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


def get_data_for_isz(date: str) -> dict:
    """
    获取可预订的场地信息
    """
    time_range = {"start_time": "07:00", "end_time": "22:30"}  # 场地的运营时间范围
    check_data = str_to_timestamp(date)
    timestamp = math.trunc(time.time() * 1000)
    nonce = gen_nonce(timestamp)
    params = {
        "salesItemId": SALES_ITEM_ID,
        "curDate": str(check_data),
        "venueGroupId": "",
        "t": str(timestamp)
    }
    param_str = f"salesItemId={SALES_ITEM_ID}&curDate={check_data}&venueGroupId=&t={str(timestamp)}"  # 仅用于签名
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
        "referer": F"https://isz.ydmap.cn/booking/schedule/{SALES_ID}?salesItemId={SALES_ITEM_ID}",
        "sec-fetch-dest": "empty"
    }
    url = "https://isz.ydmap.cn/srv100352/api/pub/sport/venue/getVenueOrderList"
    print(url)
    print(params)
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    response = requests.get(url, headers=headers, params=params, timeout=5)
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
                elif venue_id == 117557:
                    # 大沙河异常场地数据剔除
                    continue
                elif venue_id == 104867:
                    # 网羽中心异常场地数据剔除
                    continue
                elif venue_id == 102930:
                    # 香蜜6号场
                    continue
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
        return {}


def is_time_range_contained(range1, range2):
    """
    检查第一个时间范围是否被第二个时间范围包含。
    :param range1: 第一个时间范围列表，例如 ["08:00", "10:00"]
    :param range2: 第二个时间范围列表，例如 ["08:00", "12:00"]
    :return: 如果第一个时间范围被第二个时间范围包含，返回 True，否则返回 False
    """
    print(f"checking {range1} in {range2}")
    # 将时间字符串转换为 datetime 对象
    time_format = "%H:%M"
    start1 = datetime.datetime.strptime(range1[0], time_format)
    end1 = datetime.datetime.strptime(range1[1], time_format)
    start2 = datetime.datetime.strptime(range2[0], time_format)
    end2 = datetime.datetime.strptime(range2[1], time_format)

    # 检查第一个时间范围是否被第二个时间范围包含
    res = start2 <= start1 and end1 <= end2
    print(res)
    return res


def main_handler(event, context):
    """
    云函数入口
    :param event:
    :param context:
    :return:
    """
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))

    print(f"Received event: {event}")
    print(f"Received context: {str(context)}")

    if event['httpMethod'] == 'POST':
        # 读取输入参数
        input_data = json.loads(event.get('body'))
        print(f"input_data: {input_data}")
        place_name = input_data.get('place_name')
        date = input_data.get('date')  # 2023-01-01
        start_time = input_data.get('start_time')
        end_time = input_data.get('end_time')
        if date and start_time and end_time and place_name:
            pass
        else:
            raise Exception(f"input data wrong")

        # 执行函数功能
        try:
            # 查询相关的场地信息
            if place_name == '大沙河':
                data = get_data_for_isz(date)
                print(data)
            else:
                return {"code": -1, "data": None, "msg": f"不支持{place_name}的查询"}

            # 检查查询的时间段是否可预定
            input_time_range = [start_time, end_time]
            is_input_time_range_free = False
            for court_index, time_slot_list in data.items():
                for time_slot in time_slot_list:
                    if is_time_range_contained(input_time_range, time_slot):
                        is_input_time_range_free = True
                        break
                    else:
                        pass
            if is_input_time_range_free:
                output_data = f"{place_name} {start_time}~{end_time} 场地空闲中"
            else:
                output_data = f"{place_name} {start_time}~{end_time} 场地已被预定"
            return {"code": 0, "data": output_data, "msg": "success"}
        except Exception as error:  # pylint: disable=broad-except
            return {"code": -1, "data": None, "msg": str(error)}
    else:
        return {"code": -2, "data": None, "msg": "only support post"}
