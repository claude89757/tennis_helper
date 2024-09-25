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
    print("First line infos:", first_line_infos)
    docs = get_docs_operator()
    response = docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", first_line_infos)
    print("Update cell response:", response)

    # Specify the folder path
    folder_path = "./"
    # List all files in the folder
    file_names = os.listdir(folder_path)
    print("Files in folder:", file_names)
    court_infos = {}
    expired_cell_key_list = []
    # Process each file and read its content
    for file_name in file_names:
        if "available_court" in file_name:
            print(f"Processing file: {file_name}")
            court_name = file_name.split('_')[0]
            # Combine the file path
            file_path = os.path.join(folder_path, file_name)
            # Open the file and read its content
            with open(file_path, "r") as f:
                content = f.read()
            # Process the file content
            print(f"File {file_name} content:\n{content}")
            json_str = content.replace("'", '"')
            print(f"JSON string:\n{json_str}")
            try:
                available_tennis_court_slice_infos = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_name}: {e}")
                continue
            print(f"Parsed data from {file_name}:", available_tennis_court_slice_infos)
            for check_date_str, data in available_tennis_court_slice_infos.items():
                try:
                    col_index = COLUMN[date_str_list.index(check_date_str)+1]
                except ValueError as error:
                    print(f"Date {check_date_str} not in date_str_list: {error}")
                    continue
                print(f"Processing date {check_date_str}: column {col_index}")
                for court_index, slot_list in data.items():
                    if slot_list:
                        print(f"Court index {court_index} has slots: {slot_list}")
                        # Get the court number
                        try:
                            court_num = COURT_NAME_INFOS.get(int(court_index), court_index).split("号")[0]
                        except ValueError as error:
                            court_num = str(court_index).split("号")[0]
                        print(f"Court number: {court_num}")

                        hour_slot_list = []
                        for slot in slot_list:
                            hsl = split_time_range(slot)
                            print(f"Splitting slot {slot} into hours: {hsl}")
                            hour_slot_list.extend(hsl)
                        print(f"Hour slot list: {hour_slot_list}")
                        for hour_slot in hour_slot_list:
                            try:
                                row_index = TIME_SLOTS.index(f"{hour_slot[0]}~{hour_slot[1]}") + 2
                            except ValueError as error:
                                print(f"Time slot {hour_slot[0]}~{hour_slot[1]} not in TIME_SLOTS: {error}")
                                continue
                            print(f"Row index for time slot {hour_slot[0]}~{hour_slot[1]}: {row_index}")
                            cell_key = f"{col_index}{row_index}"
                            # For current day's time, check if it's expired
                            if col_index == 'B':
                                current_hour = datetime.datetime.now().hour
                                slot_hour = int(hour_slot[0].split(':')[0])
                                if current_hour >= slot_hour:
                                    # Already expired
                                    expired_cell_key_list.append(cell_key)
                            if cell_key in court_infos:
                                court_infos[cell_key].append([court_name, court_num])
                            else:
                                court_infos[cell_key] = [[court_name, court_num]]
                    else:
                        print(f"Court index {court_index} has no slots.")
        else:
            # Do not process other files
            pass

    # Fetch and process data from GitHub
    print("Fetching data from GitHub...")
    # Fetch the data from GitHub
    response = requests.get('https://raw.githubusercontent.com/claude89757/tennis_data/refs/heads/main/isz_data_infos.json')
    if response.status_code != 200:
        print(f"Failed to fetch data from GitHub, status code: {response.status_code}")
        exit(1)
    github_data_str = response.text
    print("Raw GitHub data:", github_data_str[:500])  # Print first 500 characters for brevity

    # Preprocess the data
    # Replace True/False with true/false and None with null
    github_data_str = github_data_str.replace('False', 'false').replace('True', 'true').replace('None', 'null')

    # Use regex to replace single quotes with double quotes,
    # but skip any single quotes that are within words
    github_data_str = re.sub(r"(?<!\w)'([^']*)'(?!\w)", r'"\1"', github_data_str)
    print("Processed GitHub data (first 500 chars):", github_data_str[:500])

    # Now attempt to parse the data
    try:
        github_data_dict = json.loads(github_data_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data from GitHub: {e}")
        exit(1)
    print("Loaded GitHub data successfully.")
    print("Parsed GitHub data keys:", list(github_data_dict.keys()))

    # Process the GitHub data
    for center_name, center_data in github_data_dict.items():
        print(f"Processing center: {center_name}")
        court_infos_data = center_data.get('court_infos', {})
        print(f"Center {center_name} has court infos for dates: {list(court_infos_data.keys())}")
        for date_key, courts_data in court_infos_data.items():
            print(f"Processing date key: {date_key}")
            # date_key is something like '星期三(09-25)'
            date_match = re.search(r'\((\d{2}-\d{2})\)', date_key)
            if not date_match:
                print(f"Date key {date_key} does not match expected format.")
                continue
            date_part = date_match.group(1)  # '09-25'
            # Construct 'YYYY-MM-DD'
            year = datetime.datetime.now().year
            check_date = datetime.datetime.strptime(f'{year}-{date_part}', '%Y-%m-%d')
            check_date_str = check_date.strftime('%Y-%m-%d')
            print(f"Extracted date: {check_date_str}")
            if check_date_str not in date_str_list:
                print(f"Date {check_date_str} not in date_str_list: {date_str_list}")
                continue  # Date not in the next 7 days
            col_index = COLUMN[date_str_list.index(check_date_str)+1]
            print(f"Column index for date {check_date_str}: {col_index}")
            for court_name_full, time_slots in courts_data.items():
                print(f"Processing court: {court_name_full}")
                court_num = court_name_full.replace('号网球场', '').strip()
                for time_slot_info in time_slots:
                    if not time_slot_info.get('selectable', False):
                        print(f"Time slot {time_slot_info.get('time')} is not selectable.")
                        continue  # Skip if not selectable
                    time_range_str = time_slot_info.get('time')
                    if not time_range_str:
                        print(f"No time range in time slot info: {time_slot_info}")
                        continue
                    print(f"Processing time slot: {time_range_str}")
                    # time_range_str is something like '07:00-09:00' or '07:00-07:30'
                    start_time_str, end_time_str = time_range_str.strip().split('-')
                    time_range_list = [start_time_str.strip(), end_time_str.strip()]
                    # Split the time range into hourly slots
                    hour_slot_list = split_time_range(time_range_list)
                    print(f"Splitting time range {time_range_list} into hourly slots: {hour_slot_list}")
                    for hour_slot in hour_slot_list:
                        time_slot_str = f"{hour_slot[0]}~{hour_slot[1]}"
                        try:
                            row_index = TIME_SLOTS.index(time_slot_str) + 2
                        except ValueError as error:
                            print(f"Time slot {time_slot_str} not in TIME_SLOTS: {error}")
                            continue  # Time slot not in TIME_SLOTS
                        print(f"Row index for time slot {time_slot_str}: {row_index}")
                        cell_key = f"{col_index}{row_index}"
                        # Check if the time slot is expired
                        if check_date_str == datetime.datetime.now().strftime('%Y-%m-%d'):
                            current_time = datetime.datetime.now()
                            slot_start_time = datetime.datetime.strptime(hour_slot[0], '%H:%M').replace(
                                year=check_date.year, month=check_date.month, day=check_date.day)
                            if current_time >= slot_start_time:
                                expired_cell_key_list.append(cell_key)
                        if cell_key in court_infos:
                            court_infos[cell_key].append([center_name, court_num])
                        else:
                            court_infos[cell_key] = [[center_name, court_num]]

    print(f"expired_cell_key_list: {expired_cell_key_list}")
    print("Final court_infos:", court_infos)
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
                court_num_str = ','.join(sorted(set(sorted_court_num_list)))
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
        print("Updating cells with the following data:")
        for k, v in input_data_infos.items():
            print(f"{k}: {v}")
        response = docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", input_data_infos)
        print("Update cell response:", response)
    else:
        print(f"无数据更新！！！")
        