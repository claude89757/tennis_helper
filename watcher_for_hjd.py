# -*- coding: utf-8 -*-
import os
import argparse
import requests
import time
import datetime
import shelve

from config import CD_INDEX_INFOS
from sms import send_sms_for_news
from weda import get_rule_list_from_weida
from weda import update_record_info_by_id
from weda import create_record
from common import merge_time_ranges
from common import get_free_tennis_court_infos_for_hjd
from common import get_hit_court_infos


if __name__ == '__main__':
    # 梦开始地方
    run_start_time = time.time()

    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='Help Message')

    # 添加命令行参数
    parser.add_argument('--item_name', type=str, help='Item Name')
    parser.add_argument('--watch_days', type=int, help='Watch Days')
    parser.add_argument('--send_sms', type=int, help='Send SMS')

    # 解析命令行参数
    args = parser.parse_args()

    # 检查必需的参数是否输入
    if not all([args.item_name, args.watch_days, args.send_sms]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.item_name)
        print(args.watch_days)
        print(args.send_sms)

    # 每天0点-7点不巡检， 其他时间巡检
    now = datetime.datetime.now().time()
    if datetime.time(0, 0) <= now < datetime.time(7, 0):
        print('Skipping task execution between 0am and 7am')
        exit()
    else:
        print('Executing task at {}'.format(datetime.datetime.now()))

    # 从weda的数据库，获取通知规则
    rule_list = get_rule_list_from_weida(CD_INDEX_INFOS.get(args.item_name))
    rule_date_list = []
    print(f"rule_list: {len(rule_list)}")
    for rule in rule_list:
        print(rule)
    if not rule_list:
        print(f"该场地无人订阅，不触发巡检")
        exit()
    else:
        # 标记这些订阅的状态：运行中或者已过期
        for rule in rule_list:
            # 获取今天的日期
            today = datetime.date.today()
            # 将今天的日期作为check_date
            check_date = datetime.datetime.combine(today, datetime.datetime.min.time())
            # 使用check_date来判断订阅的状态
            rule_start_date = datetime.datetime.strptime(rule['start_date'], "%Y-%m-%d")
            rule_end_date = datetime.datetime.strptime(rule['end_date'], "%Y-%m-%d")
            print(f"{today} {rule['start_date']} {rule['end_date']}之间")
            if rule_start_date <= check_date <= rule_end_date:
                # 运行中
                print(f"运行中: {rule}")
                update_record_info_by_id(rule['_id'], {"status": '2'})  # 状态: 运行中
                rule_date_list.append(rule_start_date)
                rule_date_list.append(rule_end_date)
            elif check_date > rule_end_date:
                # 已过期
                print(f"已过期: {rule}")
                update_record_info_by_id(rule['_id'], {"status": '3'})  # 状态: 运行中
            else:
                # 未生效
                print(f"未生效: {rule}")
            time.sleep(0.1)
    print("-----------------------------------------")

    # 获取公网HTTPS代理
    url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt"
    response = requests.get(url)
    text = response.text.strip()
    print(text)
    proxy_list = [line.strip() for line in text.split()]
    print(proxy_list)

    # 查询空闲的球场信息
    available_tennis_court_slice_infos = {}
    min_rule_check_date = min(rule_date_list)
    max_rule_check_date = max(rule_date_list)
    print(f"rule check date: from {min_rule_check_date} to {max_rule_check_date}")
    for index in range(0, args.watch_days):
        check_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d")
        if min_rule_check_date <= check_date <= max_rule_check_date:
            # 只查询被订阅的日期的信息
            print(f"checking {check_date_str}")
        else:
            # skip
            print(f"skip checking {check_date_str}")
            continue
        available_tennis_court_slice_infos[check_date_str] = []
        free_tennis_court_infos = get_free_tennis_court_infos_for_hjd(check_date_str, proxy_list)
        available_tennis_court_slice_infos[check_date_str] = free_tennis_court_infos
        time.sleep(5)
    print(f"available_tennis_court_slice_infos: {available_tennis_court_slice_infos}")

    # 获取命中规则的场地信息
    found_court_infos = get_hit_court_infos(available_tennis_court_slice_infos, rule_list)
    print(f"found_court_infos: {found_court_infos}")

    # 确认是否发短信
    if not args.send_sms:
        print(f"不发生短信，仅测试打印")
        exit()
    else:
        pass

    # 汇总场地信息，并发送短信
    phone_slot_infos = {}
    rule_infos = {}
    for court_info in found_court_infos:
        if court_info['court_index'] == 102930:
            # 香蜜的6号场只能电话当日预定，这里先剔除
            continue
        elif court_info['court_index'] in [104300, 104301, 104302, 104475]:
            # 黄木岗的训练墙剔除
            continue
        else:
            pass
        print(court_info)
        key = f"{court_info['phone']}_{court_info['date']}"
        if phone_slot_infos.get(key):
            phone_slot_infos[key].append([court_info['start_time'], court_info['end_time']])
            rule_infos[key].append(court_info['rule_info'])
        else:
            phone_slot_infos[key] = [[court_info['start_time'], court_info['end_time']]]
            rule_infos[key] = [court_info['rule_info']]
    if not phone_slot_infos:
        print(F"无需要通知的场地信息")
    else:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信，不重复发生
        cache = shelve.open(f'{args.item_name}_cache')
        print(f"phone_slot_infos: {phone_slot_infos}")
        for phone_date, slot_list in phone_slot_infos.items():
            print(f"sending {phone_date} sms of {slot_list}")
            merge_slot_list = merge_time_ranges(slot_list)  # 可能有多个时间段，短信只发送第一个时间段
            print(f"merge_slot_list: {merge_slot_list}")
            cache_key = f"{phone_date}_{merge_slot_list[0][0]}_{merge_slot_list[0][0]}"
            if phone_date in cache:
                print(f"{cache_key} has already been sent, skipping...")
                continue
            else:
                # 执行任务
                phone = phone_date.split('_')[0]
                date = phone_date.split('_')[1]
                sms_res = send_sms_for_news([phone],
                                            [date, args.item_name, merge_slot_list[0][0], merge_slot_list[0][1]])
                print(sms_res)
                if "send success" in sms_res:
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
                    print("短信发送失败！！！！！")
                # 记录短信到weda数据库
                try:
                    create_record({"phone": phone, "sms_text": f"{date} {args.item_name} 可预定时间: "
                                                               f"{merge_slot_list[0][0]}~{merge_slot_list[0][1]}",
                                   "status": sms_res['SendStatusSet'][0]['Message']})
                except Exception as error:
                    print(f"error: {error}")
            time.sleep(1)
            # 更新本地文件缓存
            cache[phone_date] = 1
        # 关闭本地文件缓存
        cache.close()

    # 计算执行时间
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print(f"执行时间：{execution_time}秒")
