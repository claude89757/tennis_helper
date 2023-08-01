#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/14 00:41
@Author  : claude89757
@File    : refresh_rule_status.py
@Software: PyCharm
"""
import json
import time
import datetime
import fcntl

from config import CD_INDEX_INFOS
from config import ALL_RULE_FILENAME
from config import CD_ACTIVE_DAY_INFOS
from weda import get_all_rule_list
from weda import get_vip_user_list
from weda import update_record_info_by_id
from common import print_with_timestamp


if __name__ == '__main__':
    # 每天0点-7点不巡检，其他时间巡检
    now = datetime.datetime.now().time()
    if datetime.time(0, 0) <= now < datetime.time(8, 0):
        print_with_timestamp('Skipping task execution between 0am and 7am')
        # exit() test
    else:
        print_with_timestamp('Executing task at {}'.format(datetime.datetime.now()))
    run_start_time = time.time()
    updated_rule_id_list = []

    # 获取所有规则
    all_rule_list = get_all_rule_list(use_cache=False)

    # 从微搭的数据库，获取订阅规则列表，根据订阅日期更新订阅状态
    for court_name, court_index in CD_INDEX_INFOS.items():
        # 当前可巡检的日期范围
        check_date_list = []
        check_date_str_list = []
        for index in range(0, CD_ACTIVE_DAY_INFOS[court_name]):
            check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
            check_date_str_list.append(check_date_str)
            check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d")
            check_date_list.append(check_date)
        check_start_date = min(check_date_list)
        check_end_date = max(check_date_list)
        # print(f"check_date_str_list: {check_date_str_list}")
        # print(f"check_date_list: {check_date_list}")

        # print(f"{court_name} 可预定日期: {check_date_str_list} 正在更新订阅状态...")
        # 获取订阅列表, 非过期\重复的订阅列表
        rule_list = []
        for rule in all_rule_list:
            if rule['xjcd'] == str(court_index) and rule['status'] != '3' and rule['status'] != '4':
                rule_list.append(rule)
            else:
                pass

        rule_date_list = []
        print_with_timestamp(f"rule_list: {len(rule_list)}")
        if not rule_list:
            print_with_timestamp(f"该场地无人订阅，不触发刷新")
        else:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # 标记这些订阅的状态：运行中、已过期、未生效
            phone_active_rule_infos = {}
            phone_today_sms_count_infos = {}
            for rule in rule_list:
                # 判断订阅的状态，根据日期范围是否有交集
                rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
                rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
                print(f"{check_start_date} - {check_end_date} vs {rule['start_date']} - {rule['end_date']}")
                print(f"rule run day: {(check_start_date - rule_start_date).days}")
                print(rule['user_level'])
                today_send_num = rule['jrtzcs']
                total_send_num = rule['zjtzcs']
                if int((check_start_date - rule_start_date).days) >= 7 \
                        and (str(rule['user_level']) != "2" and str(rule['user_level']) != "3"):
                    print(f"over 7 days, timeout...")
                    if rule.get("status") and rule['status'] == '3':
                        pass
                    else:
                        update_record_info_by_id(rule['_id'], {"status": '3'})  # 状态: 已过期
                        updated_rule_id_list.append(rule['_id'])
                elif check_start_date > rule_end_date:
                    if rule.get("status") and rule['status'] == '3':
                        pass
                    else:
                        update_record_info_by_id(rule['_id'], {"status": '3'})  # 状态: 已过期
                        updated_rule_id_list.append(rule['_id'])
                elif total_send_num and total_send_num >= 15 \
                        and (str(rule['user_level']) != "2" and str(rule['user_level']) != "3"):
                    if rule.get("status") and rule['status'] == '6':
                        pass
                    else:
                        update_record_info_by_id(rule['_id'], {"status": '6'})  # 状态: 超月限额
                        updated_rule_id_list.append(rule['_id'])
                # elif today_send_num and today_send_num >= 3 \
                #         and (str(rule['user_level']) != "2" and str(rule['user_level']) != "3"):
                #     if rule.get("status") and rule['status'] == '5':
                #         pass
                #     else:
                #         update_record_info_by_id(rule['_id'], {"status": '5'})  # 状态: 超日限额
                #         updated_rule_id_list.append(rule['_id'])
                elif check_start_date <= rule_end_date and check_end_date >= rule_start_date:
                    # 日期范围有交集, 运行中
                    if rule.get("status") and rule['status'] == '2':
                        pass
                    else:
                        # print(f"未生效 > 运行中: {rule}")
                        update_record_info_by_id(rule['_id'], {"status": '2'})  # 状态: 运行中
                        updated_rule_id_list.append(rule['_id'])
                        rule_date_list.append(rule_start_date)
                        rule_date_list.append(rule_end_date)
                    # 记录运行中的规则
                    if phone_active_rule_infos.get(rule['phone']):
                        phone_active_rule_infos[rule['phone']].append(rule)
                    else:
                        phone_active_rule_infos[rule['phone']] = [rule]
                else:
                    # 未生效
                    pass
                if today_send_num and (str(rule['user_level']) != "2" and str(rule['user_level']) != "3"):
                    if phone_today_sms_count_infos.get(rule['phone']):
                        phone_today_sms_count_infos[rule['phone']] += today_send_num
                    else:
                        phone_today_sms_count_infos[rule['phone']] = today_send_num
                else:
                    pass
                time.sleep(0.1)
            
            # 非VIP, 每日仅可收到3条短信
            for phone, today_send_num in phone_today_sms_count_infos.items():
                if today_send_num >= 3:
                    for rule in rule_list:
                        if rule['phone'] == phone:
                            if rule.get("status") and rule['status'] == '5':
                                pass
                            else:
                                update_record_info_by_id(rule['_id'], {"status": '5'})  # 状态: 超日限额
                                updated_rule_id_list.append(rule['_id'])
                else:
                    pass
                
            # 重复的订阅进行标记
            for phone, rules in phone_active_rule_infos.items():
                sorted_rules = sorted(rules, key=lambda x: x['createdAt'], reverse=False)
                if len(sorted_rules) > 1:
                    date_range_rule_infos = {}
                    for rule in sorted_rules:
                        date_range = f"{rule['start_date']}_{rule['end_date']}"
                        if date_range_rule_infos.get(date_range):
                            date_range_rule_infos[date_range].append(rule)
                        else:
                            date_range_rule_infos[date_range] = [rule]
                    for date_range, same_date_range_rules in date_range_rule_infos.items():
                        if len(same_date_range_rules) == 1:
                            pass
                        else:
                            # 同样日期范围的，仅生效最新创建的一条
                            for rule in same_date_range_rules[1:]:
                                # print(f"运行中 > 重复订阅: {rule}")
                                if rule.get("status") and rule['status'] == '4':
                                    pass
                                else:
                                    update_record_info_by_id(rule['_id'], {"status": '4'})  # 状态: 重复订阅
                                    updated_rule_id_list.append(rule['_id'])
                else:
                    # 仅1条订阅，无需关注
                    pass
        print("-----------------------------------------")

    # 标记是否为VIP的订阅
    print(f"标记VIP订阅....")
    # 先从本地缓存读取vip列表，如果不存在，则从远端拉取
    file_name = "vip_user_list.txt"
    try:
        with open(file_name, "r") as file:
            vip_content = file.read()
            print(vip_content)
    except Exception as error:
        print_with_timestamp(f"get local proxy list error: {error}")
        vip_content = None
    if vip_content:
        pass
    else:
        # 从远程拉取，并缓存到本地
        vip_user_list = get_vip_user_list()
        msg_list = []
        with open(file_name, "w") as file:
            for vip_user in vip_user_list:
                file.write(f"{vip_user['name']} {vip_user['phone']}\n")
                msg_list.append(f"{vip_user['name']} {vip_user['phone']}")
        vip_content = "\n".join(msg_list)

    for rule in all_rule_list:
        if not rule.get('user_level') or (rule.get('user_level') and rule['user_level'] != "2"):
            if rule['phone'] in vip_content:
                # VIP用户
                update_record_info_by_id(rule['_id'], {"user_level": "2"})
                updated_rule_id_list.append(rule['_id'])
            else:
                # 非VIP用户
                pass
        else:
            # 已标记过的VIP
            pass

    print(f"updated_rule_list: {len(updated_rule_id_list)}")
    for rule in updated_rule_id_list:
        print(rule)
    cost_time = time.time() - run_start_time
    print(f"cost_time: {cost_time}")

    # 全部订阅缓存到本地, 写入文件时加写锁
    all_rule_str = json.dumps(all_rule_list)
    with open(ALL_RULE_FILENAME, 'w+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(all_rule_list)
        fcntl.flock(f, fcntl.LOCK_UN)
