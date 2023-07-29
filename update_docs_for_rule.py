#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claude89757
@File    : update_docs.py
@Software: PyCharm
"""

import datetime

from tencent_docs import get_docs_operator
from weda import get_all_rule_list
from config import CD_INDEX_INFOS

FILE_ID = "300000000$NLrsOYBdnaed"
SHEET_ID = "m17yc6"

if __name__ == '__main__':
    # 初始化第一行数据
    first_line_infos = {"A1": f"更新时间\n{datetime.datetime.now().strftime('%H:%M:%S')}",
                        "B1": "订阅场地",
                        "C1": "开始日期",
                        "D1": "结束日期",
                        "E1": "开始时间",
                        "F1": "结束时间",
                        "G1": "最短时长",
                        "H1": "订阅状态",
                        "I1": "今天短信",
                        "J1": "累计短信",
                        "K1": "手机尾号",
                        "L1": "用户等级",
                        "M1": "创建时间",
                        }

    court_name_infos = {}
    for court_name, court_index in CD_INDEX_INFOS.items():
        court_name_infos[str(court_index)] = court_name
    status_name_infos = {
        "1": "未生效",
        "2": "运行中",
        "3": "已过期",
        "4": "重复订阅",
        "5": "超日限额",
        "6": "超月限额",
    }
    user_level_infos = {
        "1": "普通用户",
        "2": "VIP",
        "3": "SVIP",
    }

    # 获取所有规则
    all_rule_list = get_all_rule_list()

    sorted_rule_list = sorted(all_rule_list, key=lambda x: x['createdAt'], reverse=True)

    index = 2
    for rule in sorted_rule_list:
        first_line_infos[f"A{index}"] = str(index-1)
        first_line_infos[f"B{index}"] = court_name_infos.get(str(rule['xjcd']), str(rule['xjcd']))
        first_line_infos[f"C{index}"] = str(rule['start_date'])
        first_line_infos[f"D{index}"] = str(rule['end_date'])
        first_line_infos[f"E{index}"] = str(rule['start_time'])
        first_line_infos[f"F{index}"] = str(rule['end_time'])
        first_line_infos[f"G{index}"] = str(rule.get('duration', 2)).replace('None', '2')
        first_line_infos[f"H{index}"] = status_name_infos.get(str(rule['status']), str(rule['status']))
        first_line_infos[f"I{index}"] = str(rule.get('jrtzcs')).replace('None', '-').split('.')[0]
        first_line_infos[f"J{index}"] = str(rule.get('zjtzcs')).replace('None', '-').split('.')[0]
        first_line_infos[f"K{index}"] = str(rule['sjwh'])
        first_line_infos[f"L{index}"] = str(user_level_infos.get(str(rule['user_level']), "普通")).replace('None', '普通')
        first_line_infos[f"M{index}"] = str(rule['createdAt'])
        index += 1

    docs = get_docs_operator()
    docs.update_cell(FILE_ID, SHEET_ID, first_line_infos)
