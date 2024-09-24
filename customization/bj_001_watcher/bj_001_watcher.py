#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""
import os
import json
import time
import datetime
import shelve
import requests
import random
import argparse

from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def send_sms_for_news(phone_num_list: list, param_list: list, template_id: str = '1856675'):
    """
    发送短信通知
    example: send_sms_for_news(["xxxxx"], param_list=["08-03", "朝阳公园网球场", "18:00", "20:00"])
    """
    secret_id = os.environ.get("TENCENT_CLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENT_CLOUD_SECRET_KEY")
    sign_name = "网球场预定助手小程序"
    try:
        cred = credential.Credential(secret_id, secret_key)

        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"
        httpProfile.reqTimeout = 30
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

        req = models.SendSmsRequest()

        req.SmsSdkAppId = "1400835675"
        req.SignName = sign_name
        req.TemplateId = template_id
        req.TemplateParamSet = param_list
        req.PhoneNumberSet = phone_num_list
        req.SessionContext = ""
        req.ExtendCode = ""
        req.SenderId = ""

        resp = client.SendSms(req)

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
        data: 包含多个时间段的列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '08:00'], ['08:00', '09:00'], ...]
    Returns:
        合并后的时间段列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '09:00'], ...]
    """
    if not data:
        return data

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
    return result


def get_free_tennis_court_data(order_date: str, proxy_list: list = None, ok_proxy_list: list = None):
    """
    查询空闲场地信息，剔除中心场的数据
    """
    success_proxy_list = []
    url = "https://app.sun-park.com/chaoyangticket/bill/all"
    headers = {
        "Host": "app.sun-park.com",
        "VERSION": "2.0.0-saas",
        "xweb_xhr": "1",
        "Tenant-Id": "10955",
        "Authorization": "Bearer 216cf50d-3f5c-4d0c-b081-a2c8560eede6",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/107.0.0.0 Safari/537.36"
                      " MicroMessenger/6.8.0(0x16080000) NetType/WIFI"
                      " MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.8(0x13080813) XWEB/1227",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Referer": "https://servicewechat.com/wx1202b9e88c8853c3/9/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    params = {
        "siteName": "",
        "sportName": "网球",
        "day": order_date,
        "stadiumId": "1"
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
                if not proxy.startswith("http://") and not proxy.startswith("https://"):
                    proxy = "http://" + proxy  # 假设代理支持 HTTP
                proxies = {"https": proxy}
                response = requests.get(url, headers=headers, params=params,
                                        proxies=proxies, verify=False, timeout=2)
                if response.status_code == 200:
                    print(f"success for {proxy}")
                    success_proxy_list.append(proxy)
                    res = response.json()
                    break
                else:
                    print(f"failed for {proxy}, status code: {response.status_code}")
                    time.sleep(1)
                    continue
            except Exception as e:
                print(f"failed for {proxy}, error: {e}")
                continue

    else:
        print("not using proxy...")
        response = requests.get(url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            res = response.json()
        else:
            raise Exception(str(response.text))

    if res:
        if res.get("code") == 0 and res.get("msg") is None:
            print("请求成功")
            data = res["data"]["data"]  # 获取嵌套的 'data' 键
            free_time_list = []

            for time_slot, courts_info in data.items():
                for court_name, bookings in courts_info.items():
                    if court_name == "中心场":
                        continue  # 跳过中心场
                    for booking in bookings:
                        status = booking['status']
                        start_time = booking['startTime']
                        end_time = booking['endTime']
                        # status == 0 表示可用
                        if status == 0:
                            free_time_list.append({
                                "court_name": court_name,
                                "time_slot": f"{start_time}-{end_time}",
                                "status": status
                            })
            return free_time_list, success_proxy_list
        else:
            print(f"请求失败, code: {res.get('code')}, msg: {res.get('msg')}")
            raise Exception("请求失败")
    else:
        raise Exception("未知异常")


if __name__ == '__main__':
    """
    主函数
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

    # 获取公网HTTPS代理列表
    url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt"
    response = requests.get(url)
    text = response.text.strip()
    lines = text.split("\n")
    proxy_list = [line.strip() for line in lines]
    random.shuffle(proxy_list)  # 每次都打乱下
    print(f"Loaded {len(proxy_list)} proxies from {url}")

    # 查询空闲的球场信息
    up_for_send_data_list = []
    ok_proxy_list = []
    for index in range(0, 4):
        current_date = datetime.datetime.now() + datetime.timedelta(days=index)
        input_date = current_date.strftime('%Y-%m-%d')
        inform_date = current_date.strftime('%m-%d')
        weekday = current_date.weekday()  # 返回星期几，0代表周一，6代表周日

        data_list, ok_proxy_list = get_free_tennis_court_data(
            input_date,
            proxy_list=proxy_list,
            ok_proxy_list=ok_proxy_list)
        time.sleep(1)
        if data_list:
            free_slot_list = []
            for data in data_list:
                start_time = data['time_slot'].split('-')[0]
                end_time = data['time_slot'].split('-')[1]
                hour_num = int(start_time.split(':')[0])

                if weekday < 5:  # 周一至周五
                    if hour_num >= 18:
                        # 只关注18点及以后的时间段
                        free_slot_list.append([start_time, end_time])
                    else:
                        pass
                else:  # 周六和周日
                    # 全天的时间段都通知
                    free_slot_list.append([start_time, end_time])

            if free_slot_list:
                merged_free_slot_list = merge_time_ranges(free_slot_list)
                up_for_send_data_list.append({"date": inform_date,
                                              "court_name": "朝阳公园网球场",
                                              "free_slot_list": merged_free_slot_list})
            else:
                pass
        else:
            pass

    up_for_send_sms_list = []
    if up_for_send_data_list:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信
        cache = shelve.open(f'/tmp/cache')
        for up_for_send_data in up_for_send_data_list:
            date = up_for_send_data['date']
            court_name = up_for_send_data['court_name']
            free_slot_list = up_for_send_data['free_slot_list']
            for free_slot in free_slot_list:
                cache_key = f"{court_name}_{date}_{free_slot[0]}_{free_slot[1]}"
                if cache_key in cache:
                    # 已通知过
                    pass
                else:
                    # 加入待发送短信队列
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
            if sms_res and "SendStatusSet" in sms_res and sms_res["SendStatusSet"][0]["Code"] == "Ok":
                print_with_timestamp("短信发送成功")
            else:
                print_with_timestamp("短信发送失败")
            time.sleep(5)
    else:
        print_with_timestamp("无需要通知的场地信息")

    # 计算整体运行耗时
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print_with_timestamp(f"Total cost time：{execution_time} s")