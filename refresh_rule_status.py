#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/14 00:41
@Author  : claudexie
@File    : refresh_rule_status.py
@Software: PyCharm
"""

import time
import datetime

from config import CD_INDEX_INFOS
from config import CD_ACTIVE_DAY_INFOS
from weda import get_rule_list_from_weida
from weda import update_record_info_by_id
from common import print_with_timestamp


if __name__ == '__main__':
    # 每天0点-7点不巡检，其他时间巡检
    now = datetime.datetime.now().time()
    if datetime.time(0, 0) <= now < datetime.time(7, 0):
        print_with_timestamp('Skipping task execution between 0am and 7am')
        # exit() test
    else:
        print_with_timestamp('Executing task at {}'.format(datetime.datetime.now()))

    # 从微搭的数据库，获取订阅规则列表，并更新状态
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
        print(f"check_date_str_list: {check_date_str_list}")
        print(f"check_date_list: {check_date_list}")

        print(f"{court_name} 可预定日期: {check_date_str_list} 正在更新订阅状态...")
        # 获取订阅列表
        rule_list = get_rule_list_from_weida(court_index)
        rule_date_list = []
        print_with_timestamp(f"rule_list: {len(rule_list)}")
        for rule in rule_list:
            print(rule)
        if not rule_list:
            print_with_timestamp(f"该场地无人订阅，不触发")
        else:
            # 标记这些订阅的状态：运行中、已过期、未生效
            for rule in rule_list:
                # 判断订阅的状态，根据日期范围是否有交集
                rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
                rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
                print(f"{check_start_date} - {check_end_date} vs {rule['start_date']} - {rule['end_date']}之间")
                if check_start_date <= rule_end_date and check_end_date >= rule_start_date:
                    # 日期范围有交集, 运行中
                    print(f"运行中: {rule}")
                    update_record_info_by_id(rule['_id'], {"status": '2'})  # 状态: 运行中
                    rule_date_list.append(rule_start_date)
                    rule_date_list.append(rule_end_date)
                elif check_start_date > rule_end_date:
                    # 已过期
                    print(f"已过期: {rule}")
                    update_record_info_by_id(rule['_id'], {"status": '3'})  # 状态: 已过期
                else:
                    # 未生效
                    print(f"未生效: {rule}")
                time.sleep(0.1)
        print("-----------------------------------------")
