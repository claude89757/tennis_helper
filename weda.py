# -*- coding: utf-8 -*-
import os
import base64
import requests
import pytz
import datetime
import json
import fcntl

from config import ALL_RULE_FILENAME
from config import WEDA_ENV
from config import WEDA_USER_DATASOURCE

TENCENT_CLOUD_SECRET_ID = os.environ.get("TENCENT_CLOUD_SECRET_ID")
TENCENT_CLOUD_SECRET_KEY = os.environ.get("TENCENT_CLOUD_SECRET_KEY")


def get_access_token():
    """
    获取access_token
    """
    access_token = os.environ.get("WEDA_ACCESS_TOKEN")
    if access_token:
        pass
    else:
        # 换取AccessToken
        token_url = f"https://lowcode-8gsauxtn5fe06776.ap-shanghai.tcb-api.tencentcloudapi.com" \
                    f"/auth/v1/token/clientCredential"
        token_headers = {
            "Content-Type": "application/json",
            "Authorization":
                f"Basic {base64.b64encode(f'{TENCENT_CLOUD_SECRET_ID}:{TENCENT_CLOUD_SECRET_KEY}'.encode()).decode()}"
        }
        token_data = {
            "grant_type": "client_credentials"
        }
        # print(token_headers)
        # print(token_url)
        token_response = requests.post(token_url, headers=token_headers, json=token_data)
        access_token = token_response.json()["access_token"]
    print(f"access_token: {access_token}")
    os.environ["WEDA_ACCESS_TOKEN"] = access_token
    return access_token


def query_data_by_filter(env_type: str, datasource_name: str, filter_str: str = None):
    """
    根据filter查询数据源记录
    :param env_type:
    :param datasource_name:
    :param filter_str:
    :return:
    """
    access_token = get_access_token()
    # 查询数据
    if filter_str:
        query_url = f"https://lowcode-8gsauxtn5fe06776.ap-shanghai.tcb-api.tencentcloudapi.com/weda/odata/v1/batch" \
                    f"/{env_type}/{datasource_name}?$filter={filter_str}"
    else:
        query_url = f"https://lowcode-8gsauxtn5fe06776.ap-shanghai.tcb-api.tencentcloudapi.com/weda/odata/v1/batch" \
                    f"/{env_type}/{datasource_name}?$orderby=updateBy desc"
    query_params = {
        "$count": 'true',
        "$top": 5000,
    }
    query_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    print(query_url)
    # print(query_params)
    query_response = requests.get(query_url, headers=query_headers, params=query_params)
    # print(query_response.status_code)
    # print(query_response.text)
    if query_response.status_code == 200:
        return query_response.json().get('value')
    else:
        raise Exception(query_response.text)


def get_active_rule_list(cd_index: int, is_vip: bool = False):
    """
    从微搭数据源获取用户的推送规则
    :parm: cd_index 场地代号，映射见全局变量
    :return:
    """
    rule_list = []
    print("getting all rules from local file...")
    # 读取文件时加读锁
    with open(ALL_RULE_FILENAME, 'r') as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        data = f.read()
        fcntl.flock(f, fcntl.LOCK_UN)
    # 将JSON格式的字符串转换为列表
    all_rule_list = json.loads(data)
    if is_vip:
        for rule in all_rule_list:
            if rule['status'] == '2' and rule['user_level'] == '2' and rule['xjcd'] == str(cd_index):
                rule_list.append(rule)
    else:
        for rule in all_rule_list:
            if rule['status'] == '2' and rule['user_level'] != '2' and rule['user_level'] != '3' \
                    and rule['xjcd'] == str(cd_index):
                rule_list.append(rule)
    return rule_list


def get_all_rule_list(use_cache: bool = True):
    """
    从微搭数据源获取用户的推送规则
    :parm: cd_index 场地代号，映射见全局变量
    :return:
    """
    print(f"getting all rule")
    if use_cache:
        print("get from local file...")
        # 读取文件时加读锁
        with open(ALL_RULE_FILENAME, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)
        # 将JSON格式的字符串转换为列表
        all_rule_list = json.loads(data)
        return all_rule_list
    else:
        beijing_tz = pytz.timezone('Asia/Shanghai')  # 北京时区
        filter_rule_list = []
        rule_list = query_data_by_filter(WEDA_ENV, WEDA_USER_DATASOURCE)
        for rule in rule_list:
            # print(rule)
            # 转换时间格式
            start_date = datetime.datetime.fromtimestamp(rule['start_date']/1000, beijing_tz).strftime("%Y-%m-%d")
            end_date = datetime.datetime.fromtimestamp(rule['end_date'] / 1000, beijing_tz).strftime("%Y-%m-%d")
            hours = rule['start_time'] // (1000 * 60 * 60)
            minutes = (rule['start_time'] // (1000 * 60)) % 60
            seconds = (rule['start_time'] // 1000) % 60
            start_time = datetime.time(hour=int(hours), minute=int(minutes), second=int(seconds)).strftime('%H:%M')
            hours = rule['end_time'] // (1000 * 60 * 60)
            minutes = (rule['end_time'] // (1000 * 60)) % 60
            seconds = (rule['end_time'] // 1000) % 60
            end_time = datetime.time(hour=int(hours), minute=int(minutes), second=int(seconds)).strftime('%H:%M')

            timestamp = rule['createdAt'] / 1000  # 将毫秒转换为秒
            created_time = datetime.datetime.fromtimestamp(timestamp, datetime.timezone(datetime.timedelta(hours=8)))
            created_time_str = created_time.strftime('%Y-%m-%d %H:%M:%S')

            # 对日期和时间进行转义
            rule['start_date'] = start_date
            rule['end_date'] = end_date
            rule['start_time'] = start_time
            rule['end_time'] = end_time
            rule['createdAt'] = created_time_str

            # 转义后的订阅
            filter_rule_list.append(rule)
        # print(f"filter_rule_list: {filter_rule_list}")
        print(f"all_rule_list: {len(filter_rule_list)}")
        return filter_rule_list


def get_vip_user_list():
    """
    从微搭数据源获取付费用户列表
    :return:
    """
    rule_list = query_data_by_filter(WEDA_ENV, "svip_user_flj50jl")
    return rule_list


def update_record_info_by_id(record_id: str, payload: dict = None):
    """
    更新数据源记录
    """
    access_token = get_access_token()
    # 更新数据
    query_url = f"https://lowcode-8gsauxtn5fe06776.ap-shanghai.tcb-api.tencentcloudapi.com/weda/odata/v1/batch" \
                f"/{WEDA_ENV}/{WEDA_USER_DATASOURCE}('{record_id}')"

    query_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    print(query_url)
    # print(payload)
    query_response = requests.patch(query_url, headers=query_headers, json=payload, timeout=5)
    print(query_response.status_code)
    # print(query_response.text)
    if query_response.status_code == 200:
        if query_response.json().get('updateCount') and query_response.json().get('updateCount') > 0:
            return query_response.json()['updateCount']
        else:
            raise Exception(query_response.text)
    else:
        raise Exception(query_response.text)


def create_record(payload: dict):
    """
    更新数据源记录
    """
    # 换取AccessToken
    access_token = get_access_token()

    # 更新数据
    query_url = f"https://lowcode-8gsauxtn5fe06776.ap-shanghai.tcb-api.tencentcloudapi.com/weda/odata/v1" \
                f"/{WEDA_ENV}/sms_38mzmt2"

    query_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    print(query_url)
    print(payload)
    query_response = requests.post(query_url, headers=query_headers, json=payload)
    print(query_response.status_code)
    print(query_response.text)
    if query_response.status_code == 201:
        return query_response.json()
    else:
        raise Exception(query_response.text)


def get_today_active_rule_list(use_cache: bool = True):
    """
    从微搭数据源获取用户的推送规则
    :parm: cd_index 场地代号，映射见全局变量
    :return:
    """
    print(f"get_today_active_rule_list")
    if use_cache:
        print("get from local file...")
        # 读取文件时加读锁
        with open(ALL_RULE_FILENAME, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)
        # 将JSON格式的字符串转换为列表
        all_rule_list = json.loads(data)
        rule_list = []
        for rule in all_rule_list:
            if rule.get('jrtzcs') and rule['jrtzcs'] > 0:
                rule_list.append(rule)
            else:
                pass
    else:
        print("get from remote...")
        rule_list = query_data_by_filter(WEDA_ENV, WEDA_USER_DATASOURCE, f"(jrtzcs gt 0)")
    print(f"rule_list: {len(rule_list)}")
    return rule_list


# testing
if __name__ == '__main__':
    get_access_token()
