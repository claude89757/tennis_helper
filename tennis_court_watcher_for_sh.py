#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""
import os
import time
import datetime
import shelve
import requests
import random
import argparse

from typing import List
from sms import send_sms_for_news
from common import print_with_timestamp


# */5 * * * * timeout 300 /usr/bin/python3 /home/lighthouse/tennis_helper/tennis_court_watcher_for_sh.py --phone "xxx"  >> /home/lighthouse/tennis_helper/logs/sh_001_$(date +\%Y-\%m-\%d).log 2>&1


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


def get_free_tennis_court_data(field_type: str, order_date: str, proxy_list: list = None, ok_proxy_list: list = None):
    """
    查询空闲场地信息
    """
    success_proxy_list = []
    url = "https://api.go-sports.cn/home/timesListNew"
    headers = {
        "Host": "api.go-sports.cn",
        "ua": os.environ["SH_001_KEY"],
        "xweb_xhr": "1",
        "User-Agent": "Chrome",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxa43e880705719304/81/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    data = {
        "venue_id": 1,
        "field_type": field_type,
        "order_date": order_date,
    }
    res = None
    if proxy_list or ok_proxy_list:
        all_proxy_list = []
        if ok_proxy_list:
            all_proxy_list.extend(ok_proxy_list)
        if proxy_list:
            all_proxy_list.extend(proxy_list)

        try_time = 1
        for proxy in all_proxy_list:
            print(f"trying for {try_time} time for {proxy}")
            try_time += 1
            try:
                proxies = {"https": proxy}
                response = requests.post(url, headers=headers, data=data, proxies=proxies, verify=False, timeout=2)
                if response.status_code == 200:
                    print(f"success for {proxy}")
                    success_proxy_list.append(proxy)
                    res = response.json()
                    break
                else:
                    print(f"failed for {proxy}")
                    time.sleep(1)
                    continue
            except Exception:  # pylint: disable=broad-except
                print(f"failed for {proxy}")
                continue

    else:
        print("no using proxy...")
        response = requests.post(url, headers=headers, data=data, verify=False)

        if response.status_code == 200:
            res = response.json()
        else:
            raise Exception(str(response.text))

    if res:
        print("请求成功:", res["msg"])
        times_list = res["data"]["times_list"]
        free_time_list = []
        for time_slot in times_list:
            # print(f"时间段: {time_slot['name']}, 状态: {time_slot['status']}, 是否选择: {time_slot['is_select']}")
            if time_slot['status'] == 1:
                free_time_list.append(time_slot)
            else:
                pass
        return free_time_list, success_proxy_list
    else:
        raise Exception("未知异常")


if __name__ == '__main__':
    # 网球场守望者开始时间
    run_start_time = time.time()
    print_with_timestamp("start to check...")

    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--phone', type=str, help='send phone number')
    # 解析命令行参数
    args = parser.parse_args()
    # 检查必需的参数是否输入
    if not all([args.phone]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.phone)

    # 获取公网HTTPS代理列表
    try:
        filename = f"https_proxies_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(filename, "r") as file:
            content = file.read()
            print(content)
    except Exception as error:
        print_with_timestamp(str(error))
        content = None
    if content:
        print_with_timestamp()
        proxy_list = [line.strip() for line in content.split()]
    else:
        proxy_list = []
    random.shuffle(proxy_list)  # 每次都打乱下
    print_with_timestamp(f"get proxy_list({len(proxy_list)}): {proxy_list}")

    # 查询空闲的球场信息
    now = datetime.datetime.now().time()
    get_start_time = time.time()
    up_for_send_data_list = []
    ok_proxy_list = []
    for filed_type in ['in', 'out']:
        for index in range(0, 3):
            check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y%m%d')
            check_date_str2 = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%m-%d')
            print(f"checking {check_date_str}")
            data_list, ok_proxy_list = get_free_tennis_court_data(filed_type, check_date_str, proxy_list=proxy_list,
                                                                  ok_proxy_list=ok_proxy_list)

            time.sleep(1)
            if data_list:
                if filed_type == 'in':
                    free_slot_list = []
                    for data in data_list:
                        hour_num = int(str(data['name']).split(':')[0])
                        start_time = str(data['name']).split('-')[0]
                        end_time = str(data['name']).split('-')[1]
                        if 9 <= hour_num <= 21:
                            free_slot_list.append([start_time, end_time])
                        else:
                            pass
                    if free_slot_list:
                        merged_free_slot_list = merge_time_ranges(free_slot_list)
                        up_for_send_data_list.append({"date": check_date_str2,
                                                      "court_name": "卢湾室内", "free_slot_list": merged_free_slot_list})
                    else:
                        pass
                else:
                    free_slot_list = []
                    for data in data_list:
                        hour_num = int(str(data['name']).split(':')[0])
                        start_time = str(data['name']).split('-')[0]
                        end_time = str(data['name']).split('-')[1]
                        if 18 <= hour_num <= 21:
                            free_slot_list.append([start_time, end_time])
                        else:
                            pass
                    if free_slot_list:
                        merged_free_slot_list = merge_time_ranges(free_slot_list)
                        up_for_send_data_list.append({"date": check_date_str2,
                                                      "court_name": "卢湾室外", "free_slot_list": merged_free_slot_list})
                    else:
                        pass
            else:
                pass

    if up_for_send_data_list:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信，不重复发生
        up_for_send_sms_list = []
        cache = shelve.open(f'sh_001_cache')
        for up_for_send_data in up_for_send_data_list:
            date = up_for_send_data['date']
            court_name = up_for_send_data['court_name']
            free_slot_list = up_for_send_data['free_slot_list']
            for free_slot in free_slot_list:
                cache_key = f"{court_name}_{date}_{free_slot[0]}"
                if cache_key in cache:
                    # 已通知过
                    pass
                else:
                    # 加入待发送短信队里
                    up_for_send_sms_list.append({"phone": args.phone,
                                                 "date": date,
                                                 "court_name": court_name,
                                                 "start_time": free_slot[0],
                                                 "end_time": free_slot[1],
                                                 })
                    # 更新本地文件缓存
                    cache[cache_key] = 1
        # 关闭本地文件缓存
        cache.close()

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
                print_with_timestamp("短信发送成功, 刷新数据库计数")
            else:
                print_with_timestamp("短信发送失败")
            time.sleep(5)
    else:
        print_with_timestamp(F"无需要通知的场地信息")
