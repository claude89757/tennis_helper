#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claude89757
@File    : update_docs.py
@Software: PyCharm
"""

import os
import re  # Import re for regular expressions
import json
import datetime
import calendar
import requests  # Import requests for fetching data from GitHub

from tencent_docs import get_docs_operator
from tencent_docs import COLUMN
from config import COURT_NAME_INFOS

# Function to generate TIME_SLOTS including half-hour intervals
def generate_time_slots(start_time_str, end_time_str, interval_minutes=30):
    time_slots = []
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M')
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M')
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + datetime.timedelta(minutes=interval_minutes)
        if next_time > end_time:
            next_time = end_time
        time_slot = f"{current_time.strftime('%H:%M')}~{next_time.strftime('%H:%M')}"
        time_slots.append(time_slot)
        current_time = next_time
    return time_slots

# Generate TIME_SLOTS from 07:00 to 22:00 with 30-minute intervals
TIME_SLOTS = generate_time_slots('07:00', '22:00', interval_minutes=30)
# Reverse the list if you want the time slots in descending order
TIME_SLOTS = TIME_SLOTS[::-1]

def split_time_range(time_range, interval_minutes=30):
    """
    Split time range into specified minute intervals, up to 22:00.
    """
    result = []
    if time_range[0] == '00:00' or time_range[1] == '00:00':
        # Ignore this special case
        return result

    start_time = datetime.datetime.strptime(time_range[0], '%H:%M')
    end_time = datetime.datetime.strptime(time_range[1], '%H:%M')

    # Cap end_time at 22:00
    end_time_limit = datetime.datetime.strptime('22:00', '%H:%M')
    if end_time > end_time_limit:
        end_time = end_time_limit

    while start_time < end_time:
        if start_time >= end_time_limit:
            break
        next_time = start_time + datetime.timedelta(minutes=interval_minutes)
        if next_time > end_time:
            next_time = end_time  # Adjust to the end time
        result.append([start_time.strftime('%H:%M'), next_time.strftime('%H:%M')])
        start_time = next_time

    return result

if __name__ == '__main__':
    # Initialize first line data
    first_line_infos = {"A1": f"刷新\n{datetime.datetime.now().strftime('%H:%M')}"}
    date_str_list = []
    check_days = 7
    for index in range(check_days):
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
    # 初始化过期单元格列表
    expired_cell_key_list = []
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
                    print(f"Error finding column index for date {check_date_str}: {error}")
                    continue
                print(f"Processing date: {check_date_str} with column {col_index}")
                for court_index, slot_list in data.items():
                    if slot_list:
                        # 获取场地号
                        try:
                            court_num_raw = COURT_NAME_INFOS.get(int(court_index), court_index)
                        except ValueError as error:
                            court_num_raw = str(court_index)
                        # Extract digits from court number
                        court_num = re.sub(r'\D', '', court_num_raw)
                        
                        print(f"Processing court {court_num} with slots {slot_list}")
                        hour_slot_list = []
                        for slot in slot_list:
                            hour_slot_list.extend(split_time_range(slot, interval_minutes=30))
                        print(f"Split into time slots: {hour_slot_list}")
                        for hour_slot in hour_slot_list:
                            try:
                                time_slot_str = f"{hour_slot[0]}~{hour_slot[1]}"
                                row_index = TIME_SLOTS.index(time_slot_str) + 2
                            except ValueError as error:
                                print(f"Error finding TIME_SLOT {time_slot_str}: {error}")
                                continue
                            print(f"Row index for time slot '{time_slot_str}': {row_index}")
                            cell_key = f"{col_index}{row_index}"
                            # 当日的时间，判断是否已经过期
                            if col_index == 'B':
                                current_time = datetime.datetime.now().strftime('%H:%M')
                                if current_time >= hour_slot[1]:
                                    # 已过期
                                    expired_cell_key_list.append(cell_key)
                                else:
                                    # 未过期
                                    pass
                            else:
                                # 非当日
                                pass
                            if court_infos.get(cell_key):
                                court_infos[cell_key].append([court_name, court_num])
                            else:
                                court_infos[cell_key] = [[court_name, court_num]]
                    else:
                        pass
        else:
            # 其他文件不处理
            pass

    # Fetch data from GitHub
    url = "https://raw.githubusercontent.com/claude89757/tennis_data/refs/heads/main/isz_data_infos.json"

    # Fetch the data
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data_str = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub: {e}")
        json_data_str = "{}"  # Use empty JSON as fallback

    # Parse the JSON data
    try:
        isz_data_infos = json.loads(json_data_str)
        print(f"Fetched data from GitHub. Courts found: {list(isz_data_infos.keys())}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        isz_data_infos = {}

    # Map Chinese weekdays to index (Monday=0)
    weekday_cn_to_num = {'星期一': 0, '星期二': 1, '星期三': 2, '星期四': 3,
                         '星期五': 4, '星期六': 5, '星期日': 6}

    # Process the data
    for venue_name, venue_data in isz_data_infos.items():
        print(f"Processing venue: {venue_name}")
        court_info = venue_data.get('court_infos', {})

        for date_str, courts in court_info.items():
            # Extract the date in 'MM-DD' format from the string
            date_part = date_str[date_str.find('(')+1:date_str.find(')')]
            # Construct the date with the current year
            date_formatted = f"{datetime.datetime.now().year}-{date_part}"
            try:
                date_obj = datetime.datetime.strptime(date_formatted, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except ValueError as e:
                print(f"Error parsing date '{date_str}': {e}")
                continue

            # Check if the date is within the dates we're interested in
            if formatted_date not in date_str_list:
                print(f"Date {formatted_date} not in date_str_list.")
                continue

            # Get the column index for the date
            try:
                col_index = COLUMN[date_str_list.index(formatted_date)+1]
            except ValueError as error:
                print(f"Error finding column index for date {formatted_date}: {error}")
                continue

            # Process courts
            for court_name, time_slots in courts.items():
                # Extract digits from court name to get court number
                court_num = re.sub(r'\D', '', court_name)
                for slot_info in time_slots:
                    if slot_info.get('status') == '可预订':
                        time_range = slot_info.get('time')
                        # Replace any tildes with hyphens and split
                        time_range_split = time_range.replace('~', '-').split('-')
                        if len(time_range_split) != 2:
                            print(f"Invalid time range '{time_range}' in court '{court_name}'.")
                            continue
                        start_time, end_time = time_range_split

                        # Ensure times are in 'HH:MM' format
                        try:
                            datetime.datetime.strptime(start_time, '%H:%M')
                            datetime.datetime.strptime(end_time, '%H:%M')
                        except ValueError as e:
                            print(f"Invalid time format in '{time_range}': {e}")
                            continue

                        # Skip time ranges starting from 22:00 or later
                        if start_time >= '22:00' or end_time > '22:00':
                            print(f"Ignoring time range '{time_range}' as it starts at or after 22:00.")
                            continue

                        # Split the time range into intervals matching your TIME_SLOTS
                        interval_minutes = 30  # Adjust as needed
                        actual_slots = split_time_range([start_time, end_time], interval_minutes)

                        for hour_slot in actual_slots:
                            time_slot_str = f"{hour_slot[0]}~{hour_slot[1]}"
                            try:
                                row_index = TIME_SLOTS.index(time_slot_str) + 2
                            except ValueError:
                                print(f"Time slot '{time_slot_str}' not found in TIME_SLOTS.")
                                continue

                            cell_key = f"{col_index}{row_index}"

                            # Check for expiration if the date is today
                            if formatted_date == datetime.datetime.now().strftime('%Y-%m-%d'):
                                current_time = datetime.datetime.now().strftime('%H:%M')
                                if current_time >= hour_slot[1]:
                                    expired_cell_key_list.append(cell_key)

                            # Update court_infos
                            court_entry = [venue_name, court_num]
                            if court_infos.get(cell_key):
                                court_infos[cell_key].append(court_entry)
                            else:
                                court_infos[cell_key] = [court_entry]
                            print(f"Added {court_entry} to cell {cell_key} for time slot '{time_slot_str}'.")
                    else:
                        pass  # status is not '可预订'

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
                # Ensure court_num contains only digits
                court_num_digits = re.sub(r'\D', '', court_num)
                if court_num_infos.get(court_name):
                    court_num_infos[court_name].append(court_num_digits)
                else:
                    court_num_infos[court_name] = [court_num_digits]
            cell_value_list = []
            for court_name, court_num_list in court_num_infos.items():
                sorted_court_num_list = sorted(set(court_num_list))
                court_num_str = ','.join(sorted_court_num_list)
                cell_value_list.append(f"{court_name} ({court_num_str})")
            cell_value = "\n".join(cell_value_list)
            if cell_key in expired_cell_key_list:
                input_data_infos[cell_key] = f"已过期\n{cell_value}"
            else:
                input_data_infos[cell_key] = cell_value
        docs.update_cell("300000000$NLrsOYBdnaed", "BB08J2", input_data_infos)
        print("Docs updated successfully.")
    else:
        print(f"无数据更新！！！")
