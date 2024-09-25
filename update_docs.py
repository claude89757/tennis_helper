#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claude89757
@File    : update_docs.py
@Software: PyCharm
"""

import os
import re
import json
import datetime
import calendar
import requests
import yaml  # Import YAML for parsing

from tencent_docs import get_docs_operator
from tencent_docs import COLUMN
from config import COURT_NAME_INFOS


TIME_SLOTS = ['21:00~22:00',
              '20:00~21:00',
              '19:00~20:00',
              '18:00~19:00',
              '17:00~18:00',
              '16:00~17:00',
              '15:00~16:00',
              '14:00~15:00',
              '13:00~14:00',
              '12:00~13:00',
              '11:00~12:00',
              '10:00~11:00',
              '09:00~10:00',
              '08:00~09:00',
              '07:00~08:00']


def split_time_range(time_range):
    """
    Split the time range into whole-hour segments and ignore partial hours.
    """
    result = []
    if time_range[0] == '00:00':
        # Ignore this special scenario
        return result
    else:
        pass

    start_time = datetime.datetime.strptime(time_range[0], '%H:%M')
    end_time = datetime.datetime.strptime(time_range[1], '%H:%M')
    # Ensure the start time is on the hour
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
    # Initialize the first row data
    first_line_infos = {"A1": f"刷新\n{datetime.datetime.now().strftime('%H:%M')}"}
    date_str_list = []
    check_days = 7
    for index in range(0, check_days):
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

    # Specify the folder path
    folder_path = "./"
    # List all files in the folder
    file_names = os.listdir(folder_path)
    court_infos = {}
    expired_cell_key_list = []
    # Process each file and read its content
    for file_name in file_names:
        if "available_court" in file_name:
            court_name = file_name.split('_')[0]
            # Combine the file path
            file_path = os.path.join(folder_path, file_name)
            # Open the file and read its content
            with open(file_path, "r") as f:
                content = f.read()
            # Process the file content
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
                        # Get the court number
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
                                # print(f"error: {error}")
                                continue
                            print(row_index)
                            cell_key = f"{col_index}{row_index}"
                            # For current day's time, check if it's expired
                            if col_index == 'B':
                                current_hour = datetime.datetime.now().hour
                                slot_hour = int(hour_slot[0].split(':')[0])
                                if current_hour >= slot_hour:
                                    # Already expired
                                    expired_cell_key_list.append(cell_key)
                                else:
                                    # Not expired
                                    pass
                            else:
                                # Not current day
                                pass
                            if court_infos.get(cell_key):
                                court_infos[cell_key].append([court_name, court_num])
                            else:
                                court_infos[cell_key] = [[court_name, court_num]]
                    else:
                        pass
        else:
            # Do not process other files
            pass
    print(f"From file: {court_infos}")
    
    # Fetch and process data from GitHub
    # Fetch the data from GitHub
    response = requests.get('https://raw.githubusercontent.com/claude89757/tennis_data/refs/heads/main/isz_data_infos.json')
    github_data_str = response.text
    
    # Load the data using yaml.safe_load
    github_data_dict = yaml.safe_load(github_data_str)

    # Process the GitHub data
    for center_name, center_data in github_data_dict.items():
        court_infos_data = center_data.get('court_infos', {})
        for date_key, courts_data in court_infos_data.items():
            # date_key is something like '星期三(09-25)'
            date_match = re.search(r'\((\d{2}-\d{2})\)', date_key)
            if not date_match:
                continue
            date_part = date_match.group(1)  # '09-25'
            # Construct 'YYYY-MM-DD'
            year = datetime.datetime.now().year
            check_date = datetime.datetime.strptime(f'{year}-{date_part}', '%Y-%m-%d')
            check_date_str = check_date.strftime('%Y-%m-%d')
            try:
                col_index = COLUMN[date_str_list.index(check_date_str)+1]
            except ValueError as error:
                continue  # Date not in the next 7 days
            for court_name, time_slots in courts_data.items():
                court_num = court_name.replace('号网球场', '').strip()
                for time_slot_info in time_slots:
                    if not time_slot_info.get('selectable', False):
                        continue  # Skip if not selectable
                    time_range_str = time_slot_info.get('time')
                    if not time_range_str:
                        continue
                    # time_range_str is something like '07:00-09:00' or '07:00-07:30'
                    start_time_str, end_time_str = time_range_str.strip().split('-')
                    time_range_list = [start_time_str.strip(), end_time_str.strip()]
                    # Split the time range into hourly slots
                    hour_slot_list = split_time_range(time_range_list)
                    for hour_slot in hour_slot_list:
                        time_slot_str = f"{hour_slot[0]}~{hour_slot[1]}"
                        try:
                            row_index = TIME_SLOTS.index(time_slot_str) + 2
                        except ValueError as error:
                            continue  # Time slot not in TIME_SLOTS
                        cell_key = f"{col_index}{row_index}"
                        # Check if the time slot is expired
                        if check_date_str == datetime.datetime.now().strftime('%Y-%m-%d'):
                            current_time = datetime.datetime.now()
                            slot_start_time = datetime.datetime.strptime(hour_slot[0], '%H:%M').replace(
                                year=check_date.year, month=check_date.month, day=check_date.day)
                            if current_time >= slot_start_time:
                                expired_cell_key_list.append(cell_key)
                        if court_infos.get(cell_key):
                            court_infos[cell_key].append([center_name, court_num])
                        else:
                            court_infos[cell_key] = [[center_name, court_num]]
    
    print(f"From github: {court_infos}")

    print(f"expired_cell_key_list: {expired_cell_key_list}")
    if court_infos:
        input_data_infos = {}
        for row_index in range(len(TIME_SLOTS)):
            for col_index in range(check_days):
                cell_key = f"{COLUMN[col_index+1]}{row_index+2}"
                input_data_infos[cell_key] = ""

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
                court_num_str = ','.join(sorted_court_num_list)
                if court_name in ["香蜜体育", '大沙河', '简上', '黄木岗', '深云文体', '深圳湾']:
                    # Court names that have been mapped
                    cell_value_list.append(f"{court_name} ({court_num_str})")
                else:
                    cell_value_list.append(f"{court_name} {len(set(sorted_court_num_list))}")
            cell_value = "\n".join(cell_value_list)
            if cell_key in expired_cell_key_list:
                input_data_infos[cell_key] = f"已过期\n{cell_value}"
            else:
                input_data_infos[cell_key] = cell_value
        docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", input_data_infos)
    else:
        print(f"无数据更新！！！")