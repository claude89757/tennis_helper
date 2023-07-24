#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/14 00:41
@Author  : claude89757
@File    : inform_rule_expired.py
@Software: PyCharm
"""

from weda import get_all_rule_list
from sms import send_sms_for_news
from weda import update_record_info_by_id

if __name__ == '__main__':
    # 获取订阅列表
    rule_list = get_all_rule_list()

    # 整理每个用户的订阅状态
    phone_rule_status_infos = {}
    phone_rule_infos = {}
    for rule in rule_list:
        phone = rule['phone']
        status = rule['status']
        if phone_rule_status_infos.get(phone):
            phone_rule_status_infos[phone].append(status)
            phone_rule_infos[phone].append(rule)
        else:
            phone_rule_status_infos[phone] = [status]
            phone_rule_infos[phone] = [rule]

    # 判断哪些用户的全部订阅都过期，如果是，发送短信提醒
    inform_phone_list = []
    for phone, rule_status_set in phone_rule_status_infos.items():
        if len(set(rule_status_set)) == 1 and rule_status_set[0] == '3':
            is_send_before = set()
            for rule in phone_rule_infos[phone]:
                print(rule)
                is_send_before.add(str(rule.get('tzgq')))
            print(f"is_send_before: {is_send_before}")
            if len(is_send_before) == 1 and list(is_send_before)[0] == '2':
                # 已通知过，跳过
                pass
            else:
                # 未通知过，需要通知
                # sms_res = send_sms_for_news([phone], [f"{len(rule_status_set)} 个"], template_id="1863727")
                # print(sms_res)
                inform_phone_list.append(phone)
                # 标记已通知过
                for rule in phone_rule_infos[phone]:
                    if rule.get("tzgq") and rule.get("tzgq") == '2':
                        pass
                    else:
                        update_record_info_by_id(rule['_id'], {"tzgq": '2'})
        else:
            pass
    print(f"send sms to {inform_phone_list} phone")
