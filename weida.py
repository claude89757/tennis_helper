# -*- coding: utf-8 -*-
import os
import base64
import requests

TENCENT_CLOUD_SECRET_ID = os.environ.get("TENCENT_CLOUD_SECRET_ID")
TENCENT_CLOUD_SECRET_KEY = os.environ.get("TENCENT_CLOUD_SECRET_KEY")


def query_data_by_filter(env_type, datasource_name, filter_str):
    """
    根据filter查询数据源记录
    :param env_type:
    :param datasource_name:
    :param filter_str:
    :return:
    """
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
    print(token_url)
    token_response = requests.post(token_url, headers=token_headers, json=token_data)
    print(token_response.text)
    access_token = token_response.json()["access_token"]

    # 查询数据
    query_url = f"https://lowcode-8gsauxtn5fe06776.ap-guangzhou.tcb-api.tencentcloudapi.com/odata/v1" \
                f"/{env_type}/{datasource_name}"
    query_params = {
        # "$filter": filter_str
    }
    query_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    print(query_url)
    query_response = requests.get(query_url, headers=query_headers, params=query_params)
    print(query_response.status_code)
    print(query_response.text)
    return query_response.json()


def get_rule_list_from_weida(xjcd: str):
    """
    从微搭数据源获取用户的推送规则
    :return:
    """
    print(f"getting rule for {xjcd}")
    rule_list = [
        {
            "name": "claude",
            "phone": "12345678",
            "start_date": "2023-07-07",
            "end_date": "2023-08-01",
            "start_time": "18:00",
            "end_time": "22:00",
            "xjcd": '大沙河公园体育中心,(开发中)深圳地铁文化公园'
         }
    ]
    # data = query_data_by_filter()
    return rule_list


# testing
if __name__ == '__main__':
    result = query_data_by_filter("prod", "reserve_x2pq8s0", "")
    print(result)
