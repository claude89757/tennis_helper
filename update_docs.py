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

# Define TIME_SLOTS with full-hour intervals
TIME_SLOTS = [
    '21:00~22:00',
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
    '07:00~08:00'
]

def split_time_range_to_half_hours(time_range):
    """
    Split time range into half-hour intervals.
    """
    result = []
    if time_range[0] == '00:00' or time_range[1] == '00:00':
        # Ignore this special case
        return result

    start_time = datetime.datetime.strptime(time_range[0], '%H:%M')
    end_time = datetime.datetime.strptime(time_range[1], '%H:%M')

    while start_time < end_time:
        next_time = start_time + datetime.timedelta(minutes=30)
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

    court_infos = {}
    # Initialize expired cell key list
    expired_cell_key_list = []

    # Function to process available slots
    def process_available_slots(court_name, court_num, available_slots, col_index, is_today):
        # Create a dictionary to store availability of half-hours for each hour
        availability = {}
        for slot in available_slots:
            half_hour_slots = split_time_range_to_half_hours(slot)
            for half_hour_slot in half_hour_slots:
                # Get the hour key (e.g., '11:00~12:00')
                slot_start = datetime.datetime.strptime(half_hour_slot[0], '%H:%M')
                slot_end = datetime.datetime.strptime(half_hour_slot[1], '%H:%M')
                hour_start = slot_start.replace(minute=0)
                hour_end = hour_start + datetime.timedelta(hours=1)
                hour_key = f"{hour_start.strftime('%H:%M')}~{hour_end.strftime('%H:%M')}"
                # Ensure hour_key is within TIME_SLOTS
                if hour_key not in TIME_SLOTS:
                    continue
                # Initialize the availability list for this hour if not present
                if hour_key not in availability:
                    availability[hour_key] = set()
                # Mark the half-hour as available (either 'first_half' or 'second_half')
                if slot_start.minute == 0:
                    availability[hour_key].add('first_half')
                else:
                    availability[hour_key].add('second_half')
        # Now, for each hour, check if both halves are available
        for hour_key, halves in availability.items():
            if halves == {'first_half', 'second_half'}:
                # Both halves are available, process this hour
                try:
                    row_index = TIME_SLOTS.index(hour_key) + 2
                except ValueError as error:
                    print(f"Error finding TIME_SLOT {hour_key}: {error}")
                    continue
                cell_key = f"{col_index}{row_index}"
                # Check for expiration if today
                if is_today:
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    hour_end = hour_key.split('~')[1]
                    if current_time >= hour_end:
                        expired_cell_key_list.append(cell_key)
                # Update court_infos
                court_entry = [court_name, court_num]
                if court_infos.get(cell_key):
                    court_infos[cell_key].append(court_entry)
                else:
                    court_infos[cell_key] = [court_entry]
                print(f"Added {court_entry} to cell {cell_key} for time slot '{hour_key}'.")

    # Process local files
    folder_path = "./"
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        if "available_court" in file_name:
            court_name = file_name.split('_')[0]
            # Read file content
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                content = f.read()
            # Process file content
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
                is_today = (check_date_str == datetime.datetime.now().strftime('%Y-%m-%d'))
                for court_index, slot_list in data.items():
                    if slot_list:
                        # Get court number
                        try:
                            court_num_raw = COURT_NAME_INFOS.get(int(court_index), court_index)
                        except ValueError as error:
                            court_num_raw = str(court_index)
                        court_num = re.sub(r'\D', '', str(court_num_raw))
                        if not court_num:
                            court_num = str(court_index)
                        print(f"Processing court {court_num} with slots {slot_list}")
                        process_available_slots(court_name, court_num, slot_list, col_index, is_today)
        else:
            # Ignore other files
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

    # Process GitHub data
    for venue_name, venue_data in isz_data_infos.items():
        print(f"Processing venue: {venue_name}")
        court_info = venue_data.get('court_infos', {})
        print(f"court_info: {court_info}")
        for date_str, courts in court_info.items():
            # Extract the date in 'MM-DD' format from the string
            date_part_match = re.search(r'\((\d{2}-\d{2})\)', date_str)
            if date_part_match:
                date_part = date_part_match.group(1)
            else:
                print(f"Invalid date format in '{date_str}'.")
                continue
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

            is_today = (formatted_date == datetime.datetime.now().strftime('%Y-%m-%d'))

            # Process courts
            for court_name, time_slots in courts.items():
                if "墙" in court_name or "训练" in court_name:
                    continue
                # Extract digits from court name to get court number
                court_num = re.sub(r'\D', '', str(court_name))
                if not court_num:
                    court_num = court_name  # Use full name if no digits
                # Collect available slots
                available_slots = []
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

                        available_slots.append([start_time, end_time])
                if available_slots:
                    print(f"Processing court {court_num} with slots {available_slots}")
                    process_available_slots(venue_name, court_num, available_slots, col_index, is_today)
                else:
                    print(f"Processing court {court_num} with no available_slots")

    print(f"expired_cell_key_list: {expired_cell_key_list}")

    if court_infos:
        input_data_infos = {}
        # Initialize cells with empty strings
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
                # If court_num_digits is empty, use court_num as is
                if not court_num_digits:
                    court_num_digits = court_num
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
