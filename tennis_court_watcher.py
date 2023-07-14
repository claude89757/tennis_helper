#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""

import os
import argparse
import requests
import time
import datetime
import shelve

from config import CD_INDEX_INFOS
from config import CD_TIME_RANGE_INFOS

from sms import send_sms_for_news
from weda import get_active_rule_list
from weda import update_record_info_by_id
from weda import create_record
from common import merge_time_ranges
from common import get_hit_court_infos
from common import print_with_timestamp
from common import get_free_tennis_court_infos_for_isz
from common import get_free_tennis_court_infos_for_hjd
from common import get_free_tennis_court_infos_for_tns
from common import get_free_tennis_court_infos_for_ks

# 读取环境变量的值
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SIGN_KEY = os.environ.get("SIGN_KEY")
KS_TOKEN = os.environ.get("KS_TOKEN")  # 酷尚网球的token可能会过期...


if __name__ == '__main__':
    # 网球场守望者开始时间
    run_start_time = time.time()

    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--app_name', type=str, help='App Name')
    parser.add_argument('--court_name', type=str, help='Tennis Court Name')
    parser.add_argument('--sales_id', type=str, help='Sales ID for isz', required=False)
    parser.add_argument('--sales_item_id', type=str, help='Sales Item ID for isz', required=False)
    parser.add_argument('--watch_days', type=int, help='Watch Days')
    parser.add_argument('--send_sms', type=int, help='Send SMS')
    # 解析命令行参数
    args = parser.parse_args()
    # 检查必需的参数是否输入
    if not all([args.app_name, args.court_name, args.watch_days, args.send_sms]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.app_name)
        print(args.court_name)
        print(args.watch_days)
        print(args.send_sms)

    # 当前可巡检的日期范围
    check_date_list = []
    check_date_str_list = []
    for index in range(0, args.watch_days):
        check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        check_date_str_list.append(check_date_str)
        check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d")
        check_date_list.append(check_date)
    check_start_date = min(check_date_list)
    check_end_date = max(check_date_list)
    print(f"check_date_str_list: {check_date_str_list}")
    print(f"check_date_list: {check_date_list}")

    # 从微搭的数据库，获取订阅规则列表
    active_rule_list = get_active_rule_list(CD_INDEX_INFOS.get(args.court_name))
    rule_date_list = []
    print_with_timestamp(f"active_rule_list: {len(active_rule_list)}")
    for rule in active_rule_list:
        print(rule)
    if not active_rule_list:
        print_with_timestamp(f"该场地无人订阅，不触发巡检")
        exit()
    else:
        # 打印运行中的规则
        for rule in active_rule_list:
            # 判断订阅的状态，根据日期范围是否有交集
            rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
            rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
            print(f"{check_start_date} - {check_end_date} vs {rule['start_date']} - {rule['end_date']}")
            rule_date_list.append(rule_start_date)
            rule_date_list.append(rule_end_date)
    # 每天0点-7点不巡检，其他时间巡检
    now = datetime.datetime.now().time()
    if datetime.time(0, 0) <= now < datetime.time(8, 0):
        print_with_timestamp('Skipping task execution between 0am and 7am')
        exit()
    else:
        print_with_timestamp('Executing task at {}'.format(datetime.datetime.now()))
    print_with_timestamp(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # 获取公网HTTPS代理列表
    url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt"
    response = requests.get(url)
    text = response.text.strip()
    proxy_list = [line.strip() for line in text.split()]
    print_with_timestamp(f"proxy_list: {proxy_list}")

    # 查询空闲的球场信息
    available_tennis_court_slice_infos = {}
    rule_check_start_date = min(rule_date_list)
    rule_check_end_date = max(rule_date_list)
    print(f"rule check date: from {rule_check_start_date} to {rule_check_end_date}")
    for index in range(0, args.watch_days):
        # 判断日期是否查询
        check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d")
        if rule_check_start_date <= check_date <= rule_check_end_date:
            # 只查询被订阅的日期的信息
            print(f"checking {check_date_str}")
        else:
            # 未被订阅的日期不查询
            print(f"skip checking {check_date_str}")
            continue
        # 根据不同的APP，选择不同的函数获取网球场信息
        time_range = CD_TIME_RANGE_INFOS.get(args.court_name)  # 网球场营业时间范围
        if args.app_name == "ISZ":
            free_tennis_court_infos = get_free_tennis_court_infos_for_isz(check_date_str, proxy_list,
                                                                          time_range=time_range,
                                                                          sales_id=args.sales_id,
                                                                          sales_item_id=args.sales_item_id)
        elif args.app_name == "HJD":
            free_tennis_court_infos = get_free_tennis_court_infos_for_hjd(check_date_str, proxy_list)
        elif args.app_name == "TNS":
            free_tennis_court_infos = get_free_tennis_court_infos_for_tns(check_date_str, proxy_list)
        elif args.app_name == "KS":
            free_tennis_court_infos = get_free_tennis_court_infos_for_ks(check_date_str, KS_TOKEN, proxy_list)
        else:
            raise Exception(f"未支持的APP: {args.app_name}")
        available_tennis_court_slice_infos[check_date_str] = free_tennis_court_infos
        time.sleep(1)
    print_with_timestamp(f"available_tennis_court_slice_infos: {len(available_tennis_court_slice_infos)}")

    # 获取命中规则的各时间段的场地信息
    found_court_infos = get_hit_court_infos(available_tennis_court_slice_infos, active_rule_list)
    print(f"found_court_infos: {found_court_infos}")

    # 确认是否发短信
    if not args.send_sms:
        print(f"不发生短信，仅测试打印")
        exit()
    else:
        pass

    # 汇总各时间段的场地信息，按照手机粒度聚合
    phone_slot_infos = {}  # 每个手机某日期命中的时间段列表
    rule_infos = {}  # 每个手机某日期命中的订阅规则列表
    for court_info in found_court_infos:
        # 剔除一些不关注的场地
        if court_info['court_index'] == 102930:
            # 香蜜的6号场只能电话当日预定，这里先剔除
            continue
        elif court_info['court_index'] in [104300, 104301, 104302, 104475]:
            # 黄木岗的训练墙剔除
            continue
        else:
            pass
        key = f"{court_info['phone']}_{court_info['date']}"  # 手机+日期作为聚合的标志
        if phone_slot_infos.get(key):
            phone_slot_infos[key].append([court_info['start_time'], court_info['end_time']])
            rule_infos[key].append(court_info['rule_info'])
        else:
            phone_slot_infos[key] = [[court_info['start_time'], court_info['end_time']]]
            rule_infos[key] = [court_info['rule_info']]

    # 根据手机发送短信提醒
    if not phone_slot_infos:
        print_with_timestamp(F"无需要通知的场地信息")
    else:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信，不重复发生
        cache = shelve.open(f'{args.court_name}_cache')
        print(f"phone_slot_infos: {len(phone_slot_infos)}")
        for phone_date, slot_list in phone_slot_infos.items():
            print(f"sending {phone_date} sms...")
            merge_slot_list = merge_time_ranges(slot_list)  # 聚合后，可能还有多个时间段，短信只发送第一个时间段
            print(f"raw_slot_list: {slot_list}")
            print(f"merged_slot_list: {merge_slot_list}")
            cache_key = f"{phone_date}_{merge_slot_list[0][0]}_{merge_slot_list[0][0]}"  # 每个时间段仅提醒一次
            if phone_date in cache:
                print(f"{cache_key} has already been sent, skipping...")
                continue
            else:
                # 执行任务
                phone = phone_date.split('_')[0]
                date = phone_date.split('_')[1]
                sms_res = send_sms_for_news([phone],
                                            [date, args.court_name, merge_slot_list[0][0], merge_slot_list[0][1]])
                print(sms_res)
                if "send success" in str(sms_res):
                    print("短信发送成功, 刷新数据库计数")
                    # 标记短信发生成功，如果单条短信命中多个规则, 仅标记第一个规则
                    rule_info_list = rule_infos.get(phone_date)
                    cur_today_send_num = rule_info_list[0].get('jrtzcs', 0)
                    cur_total_send_num = rule_info_list[0].get('zjtzcs', 0)
                    cur_today_send_num += 1
                    cur_total_send_num += 1
                    try:
                        update_record_info_by_id(rule_info_list[0]['_id'], {"jrtzcs": cur_today_send_num,
                                                                            "zjtzcs": cur_total_send_num})
                    except Exception as error:
                        print(f"error: {error}")
                else:
                    print("短信发送失败")
                # 记录短信到weda数据库
                try:
                    create_record({"phone": phone, "sms_text": f"{date} {args.court_name} 可预定时间: "
                                                               f"{merge_slot_list[0][0]}~{merge_slot_list[0][1]}",
                                   "status": sms_res['SendStatusSet'][0]['Message']})
                except Exception as error:
                    print(f"error: {error}")
            time.sleep(1)
            # 更新本地文件缓存
            cache[phone_date] = 1
        # 关闭本地文件缓存
        cache.close()

    # 计算运行耗时
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print(f"Cost time：{execution_time} s")
