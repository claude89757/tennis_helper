#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""

import argparse
import time
import datetime
import shelve
import asyncio
import fcntl
import json
import random

from config import CD_INDEX_INFOS
from config import CD_TIME_RANGE_INFOS
from redis_client import RedisClient

from sms import send_sms_for_news
from weda import get_active_rule_list
from weda import update_record_info_by_id
from weda import create_record
from config import COURT_NAME_INFOS
from common import merge_time_ranges
from common import get_hit_court_infos
from common import print_with_timestamp
from common import get_proxy_info_list
from common import get_proxy_list
from common import get_free_tennis_court_infos_for_isz
from common import get_free_tennis_court_infos_for_hjd
from common import get_free_tennis_court_infos_for_tns
from common import get_free_tennis_court_infos_for_ks
from common import get_free_tennis_court_infos_for_zjclub
from common import get_free_tennis_court_infos_for_wcjt
from common import get_free_tennis_court_infos_for_dsports
from common import get_free_tennis_court_infos_for_shanhua
from common import get_free_tennis_court_infos_for_szw


async def get_free_tennis_court_infos(app_name: str, input_check_date_str: str, input_proxy_list: list,
                                      input_time_range: list = None,
                                      input_sales_item_id: str = None,
                                      input_sales_id: str = None):
    """
    根据提供的app_name参数，调用相应的函数来获取空闲的网球场信息。
    Args:
        app_name (str): 应用名称，根据这个参数决定调用哪个函数
        input_check_date_str (str): 检查日期，字符串格式
        input_proxy_list (list): 代理列表
        input_time_range (list): 场地时间范围
        input_sales_id(str): isz专用
        input_sales_item_id(str): isz专用
    Returns:
        Future: 一个Future对象，可以在协程中等待这个对象

    Raises:
        Exception: 如果app_name的值不是预期的值，抛出一个异常
    """
    loop = asyncio.get_event_loop()
    if app_name == "ISZ":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_isz, input_check_date_str,
                                          input_proxy_list, input_time_range, input_sales_item_id, input_sales_id, )
    elif app_name == "HJD":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_hjd, input_check_date_str,
                                          input_proxy_list)
    elif app_name == "TNS":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_tns, input_check_date_str,
                                          input_proxy_list)
    elif app_name == "KS":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_ks, input_check_date_str,
                                          input_proxy_list)
    elif app_name == "ZJCLUB":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_zjclub, input_check_date_str,
                                          input_proxy_list, input_time_range, input_sales_item_id, input_sales_id, )
    elif app_name == "WCJT":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_wcjt, input_check_date_str,
                                          input_proxy_list)
    elif app_name == "DSTY":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_dsports, input_check_date_str,
                                          input_proxy_list)
    elif app_name == "SHANHUA":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_shanhua, input_check_date_str,
                                          input_proxy_list, input_time_range)
    elif app_name == "SZW":
        return await loop.run_in_executor(None, get_free_tennis_court_infos_for_szw, input_check_date_str,
                                          input_proxy_list, input_time_range)
    else:
        raise Exception(f"未支持的APP: {app_name}")


if __name__ == '__main__':
    # 获取脚本运行的时间
    start_min_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    end_min_time = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:00")

    # 网球场守望者开始时间
    run_start_time = time.time()
    print_with_timestamp("start to check...")

    redis_client = RedisClient()

    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--app_name', type=str, help='App Name')
    parser.add_argument('--court_name', type=str, help='Tennis Court Name')
    parser.add_argument('--sales_id', type=str, help='Sales ID for isz', required=False)
    parser.add_argument('--sales_item_id', type=str, help='Sales Item ID for isz', required=False)
    parser.add_argument('--watch_days', type=int, help='Watch Days')
    parser.add_argument('--send_sms', type=int, help='Send SMS', required=False)
    # 解析命令行参数
    args = parser.parse_args()
    # 检查必需的参数是否输入
    if not all([args.app_name, args.court_name, args.watch_days]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.app_name)
        print(args.court_name)
        print(args.watch_days)

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
    print_with_timestamp(f"check_date_str_list: {check_date_str_list}")
    print_with_timestamp(f"check_date_list: {check_date_list}")

    # 从微搭的数据库，获取订阅规则列表
    active_rule_list = get_active_rule_list(CD_INDEX_INFOS.get(args.court_name))

    # 从redis读取新的订阅规则
    new_rule_list = redis_client.get_json_data(key="subscriptions")
    new_rule_ids = []
    if new_rule_list:
        print("new rule==============================================================================================")
        active_new_rule_list = []
        for rule in new_rule_list:
            if rule['xjcd'] == args.court_name:
                print(rule)
                active_new_rule_list.append(rule)
                new_rule_ids.append(rule['_id'])
        print("===============================================================================================")
        active_rule_list.extend(active_new_rule_list)
    else:
        pass

    rule_date_list = []
    print_with_timestamp(f"active_rule_list: {len(active_rule_list)}")
    for rule in active_rule_list:
        print_with_timestamp(rule)
    if not active_rule_list:
        print_with_timestamp(f"该场地无人订阅，不触发巡检")
        exit()
    else:
        # 打印运行中的规则
        for rule in active_rule_list:
            # print(f"checking: {rule}")
            # 判断订阅的状态，根据日期范围是否有交集
            rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
            rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
            # print(f"{check_start_date} - {check_end_date} vs {rule['start_date']} - {rule['end_date']}")
            rule_date_list.append(rule_start_date)
            rule_date_list.append(rule_end_date)

    # 获取公网HTTPS代理列表
    if args.app_name == 'ISZ':
        proxy_list = get_proxy_info_list()  # 有md5的url信息
    else:
        proxy_list = get_proxy_list()
    print("[PROXY]=========================")
    for proxy in proxy_list[:5]:
        print(proxy)
    print("[PROXY]=========================")

    # 查询空闲的球场信息
    now = datetime.datetime.now().time()
    get_start_time = time.time()
    available_tennis_court_slice_infos = {}
    rule_check_start_date = min(rule_date_list)
    rule_check_end_date = max(rule_date_list)
    # print(f"rule check date: from {rule_check_start_date} to {rule_check_end_date}")
    # 采用协程方式查询各日期的场地信息
    last_check_date_str = (datetime.datetime.now() + datetime.timedelta(days=args.watch_days - 1)).strftime('%Y-%m-%d')
    last_check_date_str2 = (datetime.datetime.now() + datetime.timedelta(days=args.watch_days - 1)).strftime('%m-%d')

    tasks = []
    check_date_str_list = []
    loop = asyncio.get_event_loop()
    for index in range(0, args.watch_days):
        check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d")
        print(f"checking {check_date_str}")
        time_range = CD_TIME_RANGE_INFOS.get(args.court_name)
        task = loop.create_task(get_free_tennis_court_infos(args.app_name, check_date_str, proxy_list,
                                                            input_time_range=time_range,
                                                            input_sales_item_id=args.sales_item_id,
                                                            input_sales_id=args.sales_id))
        tasks.append(task)
        check_date_str_list.append(check_date_str)

    results = loop.run_until_complete(asyncio.gather(*tasks))
    for index, check_date_str in enumerate(check_date_str_list):
        # check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        available_tennis_court_slice_infos[check_date_str] = results[index]
    # 计算查询运行时间
    run_time = time.time() - get_start_time
    print_with_timestamp(f"查询耗时: {run_time:.2f}秒")
    # 输出结果
    print_with_timestamp(f"available_tennis_court_slice_infos: {len(available_tennis_court_slice_infos)}")
    print_with_timestamp(f"available_tennis_court_slice_infos: {available_tennis_court_slice_infos}")

    # 获取命中规则的各时间段的场地信息
    found_court_infos = get_hit_court_infos(available_tennis_court_slice_infos, active_rule_list)
    print(f"found_court_infos: {found_court_infos}")

    # 每天0点-8点不发短信
    if datetime.time(0, 0) <= now < datetime.time(8, 0):
        print_with_timestamp('Skipping task execution between 0am and 8am')
        redis_client.update_json_data(f"tennis_court_infos", {str(args.court_name): available_tennis_court_slice_infos},
                                      use_lock=True)
        exit()
    else:
        print_with_timestamp('Executing task at {}'.format(datetime.datetime.now()))

    # 确认是否发短信
    if not args.send_sms:
        print(f"不发生短信，仅测试打印")
        exit()
    else:
        pass

    # 汇总各时间段的场地信息，按照手机粒度聚合
    phone_slot_infos = {}  # 每个手机某日期命中的时间段列表
    up_for_send_sms_list = []
    rule_infos = {}  # 每个手机某日期命中的订阅规则列表
    court_index_infos = {}  # 每个手机某日期命中的场地老板
    today_str = datetime.datetime.now().strftime('%m-%d')
    for court_info in found_court_infos:
        # 剔除一些不关注的场地
        if court_info['court_index'] == COURT_NAME_INFOS[102930] or str(court_info['court_index']) == "102930":
            # 香蜜的6号场只能电话当日预定, 剔除掉非当日的
            if str(court_info['date']).split()[0] == today_str:
                # court_name = "香蜜电话"
                pass
            else:
                print(f"{court_info['date']} vs {today_str}")
                continue
        elif court_info['court_index'] in [104300, 104301, 104302, 104475]:
            # 黄木岗的训练墙剔除
            continue
        elif args.court_name == "深圳湾":
            # 深圳湾仅通知当日的
            if str(court_info['date']).split()[0] == today_str:
                pass
            else:
                print(f"{court_info['date']} vs {today_str}")
                continue
        elif args.court_name == "简上":
            # 深圳湾仅通知当日的
            if str(court_info['date']).split()[0] == last_check_date_str2 \
                    and datetime.time(0, 0) <= now < datetime.time(20, 3):
                continue
            else:
                pass
        else:
            pass
        key = f"{court_info['phone']}_{court_info['date']}"  # 手机+日期作为聚合的标志
        if phone_slot_infos.get(key):
            phone_slot_infos[key].append([court_info['start_time'], court_info['end_time']])
            rule_infos[key].append(court_info['rule_info'])
            court_index_infos[key].append(str(court_info['court_index']))
        else:
            phone_slot_infos[key] = [[court_info['start_time'], court_info['end_time']]]
            rule_infos[key] = [court_info['rule_info']]
            court_index_infos[key] = [str(court_info['court_index'])]
    # 对命中的规则列表进行排序，仅最新创建的优先生效
    for phone_date, rule_list in rule_infos.items():
        rule_infos[phone_date] = sorted(rule_list, key=lambda x: x['createdAt'], reverse=True)
    # print(f"rule_infos: {rule_infos}")

    # 根据手机发送短信提醒
    if not phone_slot_infos:
        print_with_timestamp(F"无需要通知的场地信息")
    else:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信，不重复发生
        # 梳理需要发送的短信列表
        cache = shelve.open(f'{args.court_name}_cache')
        for phone_date, slot_list in phone_slot_infos.items():
            rule_info_list = rule_infos.get(phone_date)  # 一个手机号，只能命中最新的规则
            latest_rule = rule_info_list[0]
            print(f"{phone_date} rule_info_list: {latest_rule}")
            merge_slot_list = merge_time_ranges(slot_list)  # 聚合后，可能还有多个时间段，短信只发送第一个时间段
            # print(f"raw_slot_list: {slot_list}")
            # print(f"merged_slot_list: {merge_slot_list}")
            # 剔除不符合要求的时间段，过大或者过小
            print(f"merge_slot_list: {merge_slot_list}")
            filter_merge_slot_list = []
            for slot in merge_slot_list:
                time1 = datetime.datetime.strptime(slot[0], '%H:%M')
                time2 = datetime.datetime.strptime(slot[1], '%H:%M')
                # 计算时间差
                duration = time2 - time1
                # 将时间差转换为小时数的浮点数
                hours = duration.total_seconds() / 3600
                print(f"hours: {hours}")
                if hours > 12:
                    # 这类场地默认没人需要打， 过滤
                    print_with_timestamp(f"时长过大：{hours}")
                elif latest_rule.get('duration') and hours < int(latest_rule.get('duration')):
                    # 小于订阅的时长pass
                    print_with_timestamp(f"{phone_date} 小于订阅时长：{latest_rule.get('duration')}")
                elif latest_rule.get('duration') and hours >= int(latest_rule.get('duration')):
                    filter_merge_slot_list.append(slot)
                elif not latest_rule.get('duration') and hours < 2:
                    # 默认仅2小时以上的场地
                    print_with_timestamp(f"{phone_date} 默认仅2小时以上的场地")
                else:
                    filter_merge_slot_list.append(slot)
            print(f"filter_merge_slot_list: {filter_merge_slot_list}")
            # print(f"hit rule: {rule_info_list}")
            cache_key = f"{phone_date}_{merge_slot_list[0][0]}"  # 每个时间段仅提醒一次
            if cache_key in cache:
                print_with_timestamp(f"{cache_key} has already been sent, skipping...")
                continue
            elif not filter_merge_slot_list:
                print_with_timestamp(f"{cache_key} too short slot duration, skipping ...")
                continue
            else:
                court_index_list = court_index_infos.get(phone_date)
                if len(set(court_index_list)) == 1 and list(court_index_list)[0] \
                        and (list(court_index_list)[0] == COURT_NAME_INFOS[102930]
                             or list(court_index_list)[0] == "102930"):
                    send_court_name = "香蜜电话"
                else:
                    send_court_name = args.court_name

                # 加入待发送短信队里
                phone = phone_date.split('_')[0]
                date = phone_date.split('_')[1]
                start_time = merge_slot_list[0][0]
                end_time = merge_slot_list[0][1]
                if datetime.time(0, 0) <= now < datetime.time(9, 3) \
                        and args.court_name in ["香蜜体育", "黄木岗", "莲花体育", "香蜜电话"]:
                    # 未开放预定，不推送消息
                    continue
                else:
                    if str(latest_rule['user_level']) == '2' or str(latest_rule['user_level']) == 'VIP':
                        # VIP规则，直接推送
                        up_for_send_sms_list.append({"phone": phone,
                                                     "date": date,
                                                     "court_name": send_court_name,
                                                     "start_time": start_time,
                                                     "end_time": end_time,
                                                     "rule_start_date": latest_rule['start_date'],
                                                     "rule_end_date": latest_rule['end_date']})
                    else:
                        # 非VIP的情况下，随机50%的概率决定是否推送
                        if random.random() < 0.5:
                            up_for_send_sms_list.append({"phone": phone,
                                                         "date": date,
                                                         "court_name": send_court_name,
                                                         "start_time": start_time,
                                                         "end_time": end_time,
                                                         "rule_start_date": latest_rule['start_date'],
                                                         "rule_end_date": latest_rule['end_date']})
                # 更新本地文件缓存
                cache[cache_key] = 1
        # 关闭本地文件缓存
        cache.close()

        # 根据优先级策略，发送短信
        sorted_up_for_send_sms_list = sorted(up_for_send_sms_list,
                                             key=lambda x: datetime.datetime.strptime(x['rule_end_date'], '%Y-%m-%d'),
                                             reverse=False)
        send_sms_start_time = time.time()
        rule_send_count_infos = {}
        try_send_sms_list = []
        for sms_info in sorted_up_for_send_sms_list:
            print(f"sending {sms_info}...")
            phone = sms_info['phone']
            date = sms_info['date']
            court_name = sms_info['court_name']
            start_time = sms_info['start_time']
            end_time = sms_info['end_time']
            rule_info_list = rule_infos.get(f"{phone}_{date}")

            if court_name == "香蜜电话":
                continue
            else:
                pass

            # 最新的订阅生效
            valid_rule = rule_info_list[0]
            rule_id = valid_rule['_id']

            sms_res = send_sms_for_news([phone], [date, court_name, start_time, end_time])
            print(sms_res)
            if "send success" in str(sms_res):
                print_with_timestamp("短信发送成功, 刷新数据库计数")
                # 标记短信发生成功，如果单条短信命中多个规则, 仅标记第一个规则
                if rule_send_count_infos.get(rule_id):
                    rule_send_count_infos[rule_id] += 1
                else:
                    rule_send_count_infos[rule_id] = 1
            else:
                print_with_timestamp("短信发送失败")

            if str(valid_rule['user_level']) == '2':
                try_send_sms_list.append([phone,
                                          f"[vip] {date} {court_name} 可预定时间: {start_time}~{end_time}",
                                          sms_res['SendStatusSet'][0]['Message']])
            else:
                try_send_sms_list.append([phone,
                                          f"{date} {court_name} 可预定时间: {start_time}~{end_time}",
                                          sms_res['SendStatusSet'][0]['Message']])
            time.sleep(1)
        send_sms_end_time = time.time()
        send_sms_cost_time = send_sms_end_time - send_sms_start_time
        print_with_timestamp(f"发送短信耗时：{send_sms_cost_time: 2f} s")

        # 记录短信到weda数据库
        for sms_info in try_send_sms_list:
            try:
                create_record({"phone": sms_info[0], "sms_text": sms_info[1], "status": sms_info[2]})
            except Exception as error:
                print_with_timestamp(f"record sms error: {error}")

        # 刷新订阅的计数器
        for rule in active_rule_list:
            if rule_send_count_infos.get(rule['_id']) and rule['_id'] not in new_rule_ids:
                rule_send_count = rule_send_count_infos[rule['_id']]
                cur_rule_today_send_num = rule['jrtzcs']
                cur_rule_total_send_num = rule['jrtzcs']
                try:
                    if cur_rule_today_send_num:
                        update_record_info_by_id(rule['_id'], {"jrtzcs": cur_rule_today_send_num + rule_send_count})
                    else:
                        update_record_info_by_id(rule['_id'], {"jrtzcs": rule_send_count})
                    if cur_rule_total_send_num:
                        update_record_info_by_id(rule['_id'], {"zjtzcs": cur_rule_total_send_num + rule_send_count})
                    else:
                        update_record_info_by_id(rule['_id'], {"zjtzcs": rule_send_count})
                except Exception as error:
                    print_with_timestamp(f"record rule_today_send_count_infos error: {error}")
            elif rule_send_count_infos.get(rule['_id']) and rule['_id'] in new_rule_ids:
                rule_send_count = rule_send_count_infos[rule['_id']]
                cur_rule_today_send_num = rule['jrtzcs'] + rule_send_count
                cur_rule_total_send_num = rule['zjtzcs'] + rule_send_count
                updates = {
                    'jrtzcs': cur_rule_today_send_num,
                    'zjtzcs': cur_rule_total_send_num,
                }
                redis_client.update_subscription_list("subscriptions", rule['_id'], updates, use_lock=True)
            else:
                pass

    # 打开文件，如果文件不存在则创建
    with open(f"{args.court_name}_available_court.txt", "w") as file:
        # 尝试获取文件锁，如果锁已被其他进程持有，则立即返回
        try:
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            print("Unable to acquire lock")
        else:
            # 写入新的内容
            file.write(json.dumps(available_tennis_court_slice_infos))

            # 释放文件锁
            fcntl.flock(file, fcntl.LOCK_UN)

    redis_client.update_json_data(f"tennis_court_infos", {str(args.court_name): available_tennis_court_slice_infos},
                                  use_lock=True)

    # 计算整体运行耗时
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print_with_timestamp(f"Total cost time：{execution_time} s")
