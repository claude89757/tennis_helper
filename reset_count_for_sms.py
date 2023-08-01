#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/11 21:09
@Author  : claude89757
@File    : reset_count_for_sms.py
@Software: PyCharm
"""
import os
import time

from weda import get_today_active_rule_list
from weda import update_record_info_by_id

# 读取指定环境变量的值
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SIGN_KEY = os.environ.get("SIGN_KEY")


if __name__ == '__main__':
    # 明天凌晨1点，每条订阅的"今日通知短信"置0
    # 查询今日通知了短信的订阅
    rule_list = get_today_active_rule_list(use_cache=True)
    # 今日通知了短信的订阅计数置零
    for rule in rule_list:
        print(f"setting {rule}")
        update_record_info_by_id(rule['_id'], {"jrtzcs": 0})
        time.sleep(1)
