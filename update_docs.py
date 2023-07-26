#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claude89757
@File    : update_docs.py
@Software: PyCharm
"""

import os
import json
import datetime
import calendar

from tencent_docs import get_docs_operator
from tencent_docs import COLUMN
from config import COURT_NAME_INFOS


TIME_SLOTS = [
    "07:00~08:00",
    "08:00~09:00",
    "09:00~10:00",
    "10:00~11:00",
    "11:00~12:00",
    "12:00~13:00",
    "13:00~14:00",
    "14:00~15:00",
    "15:00~16:00",
    "16:00~17:00",
    "17:00~18:00",
    "18:00~19:00",
    "19:00~20:00",
    "20:00~21:00",
    "21:00~22:00",
]


def split_time_range(time_range):
    """
    分割时间段位整个小时的时间段，并忽略部分不满足一小时的时间段
    """
    start_time = datetime.datetime.strptime(time_range[0], '%H:%M')
    end_time = datetime.datetime.strptime(time_range[1], '%H:%M')
    result = []

    # 确保开始时间为整小时
    if start_time.minute != 0:
        start_time = start_time + datetime.timedelta(hours=1) - datetime.timedelta(minutes=start_time.minute)

    while start_time < end_time:
        next_hour = start_time + datetime.timedelta(hours=1)
        if next_hour > end_time:
            break
        result.append([start_time.strftime('%H:%M'), next_hour.strftime('%H:%M')])
        start_time = next_hour

    return result


if __name__ == '__main__':
    # 初始化第一行数据
    first_line_infos = {"A1": f"更新时间\n{datetime.datetime.now().strftime('%H:%M:%S')}"}
    date_str_list = []
    for index in range(0, 7):
        date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%Y-%m-%d')
        date_str_list.append(date_str)
        simple_date_str = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%m-%d')
        weekday = calendar.day_name[datetime.datetime.strptime(date_str, '%Y-%m-%d').date().weekday()]
        weekday_cn = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四',
                      'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'}[weekday]
        date_and_weekday = f'{simple_date_str}\n{weekday_cn}'
        first_line_infos[f"{COLUMN[index+1]}1"] = date_and_weekday
    print(first_line_infos)
    docs = get_docs_operator()
    docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", first_line_infos)

    # 指定文件夹路径
    folder_path = "./"
    # 列出文件夹中的所有文件
    file_names = os.listdir(folder_path)
    court_infos = {}
    # 遍历每个文件并读取其内容
    for file_name in file_names:
        if "available_court" in file_name:
            court_name = file_name.split('_')[0]
            # 拼接文件路径
            file_path = os.path.join(folder_path, file_name)
            # 打开文件并读取内容
            with open(file_path, "r") as f:
                content = f.read()
            # 处理文件内容
            print(f"File {file_name}\n{content}")
            json_str = content.replace("'", '"')
            print(json_str)
            available_tennis_court_slice_infos = json.loads(json_str)
            for check_date_str, data in available_tennis_court_slice_infos.items():
                try:
                    col_index = COLUMN[date_str_list.index(check_date_str)+1]
                except ValueError as error:
                    print(f"error: {error}")
                    continue
                print(f"{check_date_str}: {col_index}")
                for court_index, slot_list in data.items():
                    if slot_list:
                        # 获取场地号
                        try:
                            court_num = COURT_NAME_INFOS.get(int(court_index), court_index).split("号")[0]
                        except ValueError as error:
                            court_num = str(court_index).split("号")[0]
                            
                        print(slot_list)
                        hour_slot_list = []
                        for slot in slot_list:
                            hour_slot_list.extend(split_time_range(slot))
                        print(hour_slot_list)
                        for hour_slot in hour_slot_list:
                            try:
                                row_index = TIME_SLOTS.index(f"{hour_slot[0]}~{hour_slot[1]}") + 2
                            except ValueError as error:
                                print(f"error: {error}")
                                continue
                            print(row_index)
                            cell_key = f"{col_index}{row_index}"
                            if court_infos.get(cell_key):
                                court_infos[cell_key].append([court_name, court_num])
                            else:
                                court_infos[cell_key] = [[court_name, court_num]]
                    else:
                        pass
        else:
            # 其他文件不处理
            pass
    if court_infos:
        input_data_infos = {}
        for cell_key, data_list in court_infos.items():
            court_num_infos = {}
            for data in data_list:
                court_name = data[0]
                court_num = data[1]
                if court_num_infos.get(court_name):
                    court_num_infos[court_name].append(court_num)
                else:
                    court_num_infos[court_name] = [court_num]
            cell_value_list = []
            for court_name, court_num_list in court_num_infos.items():
                sorted_court_num_list = sorted(court_num_list)
                print({','.join(sorted_court_num_list)})
                cell_value_list.append(f"{court_name} {len(set(sorted_court_num_list))}")
            cell_value = "\n".join(cell_value_list)
            input_data_infos[cell_key] = cell_value
        docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", input_data_infos)
    else:
        print(f"无数据更新！！！")
