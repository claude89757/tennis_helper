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

if __name__ == '__main__':
    # 获取订阅列表
    rule_list = get_all_rule_list()

    # 整理每个用户的订阅状态
    phone_rule_status_infos = {}
    for rule in rule_list:
        phone = rule['phone']
        status = rule['status']
        if phone_rule_status_infos.get(phone):
            phone_rule_status_infos[phone].append(status)
        else:
            phone_rule_status_infos[phone] = [status]

    # 判断哪些用户的全部订阅都过期，如果是，发送短信提醒
    inform_phone_list = []
    for phone, rule_status_set in phone_rule_status_infos.items():
        if len(set(rule_status_set)) == 1 and rule_status_set[0] == '3':
            sms_res = send_sms_for_news([phone], [f"{len(rule_status_set)} 个"], template_id="1863727")
            print(sms_res)
            inform_phone_list.append(phone)
        else:
            pass
    print(f"send sms to {inform_phone_list} phone")
