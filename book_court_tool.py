#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/25 20:50
@Author  : claudexie
@File    : book_court_tool.py
@Software: PyCharm
"""
import math
import time
import json
import base64
import urllib

from common import clock_to_timestamp
from common import str_to_timestamp


def base64_encode(raw):
    return str(base64.b64encode(bytes(raw, encoding='utf-8')), 'utf-8')


def url_encode(raw):
    return urllib.parse.quote(raw, safe='')


def build_set_value_query(begin, end, order_date, verify, row_index, book_info: BookingInfo):
    """
    构造预约请求的 payload
    :param begin: 开始时间戳
    :param end:  结束时间戳
    :param order_date:  预约日期, 格式为 yyyy-MM-dd
    :param book_info: 预约场地信息
    :param verify: 字段表示了验证码的验证方法, 1 表示滑块, 2 表示华容道, 3 表示图标, 4 表示文字
    :param row_index:
    """
    row_span = int((int(end) - int(begin)) / 1000 / 3600)
    # 需要注意的是, ifVerification 字段表示了验证码的验证方法, 1 表示滑块, 2 表示华容道, 3 表示图标, 4 表示文字
    # 该字段有可能会根据前端发布而变化, 最好提前在页面中随便预约一个场地试试当前的验证方式
    # 只有使用正确的验证方式, 最终生成的 url 才有效
    query_data = {
        "bookStartTime": 0, "ifVerification": verify, "list": [{
            "salesId": book_info.sales_id, "platformParentId": 0, "venueId": book_info.field_id,
            "orderDate": order_date, "startTime": begin, "endTime": end,
            "colspan": 1, "rowspan": row_span, "colIndex": book_info.col_index, "rowIndex": row_index,
            "selectPubStudy": False, "validPubStudy": False, "faceValidMode": 0
        }], "selectSysUser": 0, "salesId": book_info.sales_id, "salesItemId": book_info.sales_item_id
    }
    raw_value = json.dumps(query_data, separators=(',', ':'))
    print(f'raw_value: {raw_value}')
    value = base64_encode(url_encode(raw_value))
    return value


def send_request(begin: str, end: str, buy_date: str, verify: int, book_info: BookingInfo):
    try:
        begin_timestamp = clock_to_timestamp(begin)
        end_timestamp = clock_to_timestamp(end)
        row_index = 2 * (int(end.split(":")[0]) - book_info.raw_index_base) - 1
        buy_timestamp = str_to_timestamp(buy_date)
        timestamp = math.trunc(time.time() * 1000)
        value = build_set_value_query(begin_timestamp, end_timestamp, buy_timestamp, verify,
                                      row_index, book_info)
        nonce = gen_nonce(timestamp)
        cache_key = base64_encode(nonce)
        nonce = nonce.replace('-', '')
        param = f'isolationUser=0&key={cache_key}&value={value}'
        signature = signature2(str(timestamp), nonce, param)
        response = requests.post(
            url=f"https://{book_info.host}/srv100801/api/pub/sport/venue/setValue",
            headers={
                "Host": book_info.host,
                "Connection": "keep-alive",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "Openid-Token": "Openid-Token",
                "Entry-Tag": "",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua-platform": "\"macOS\"",
                "Origin": book_info.url,
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": f"{book_info.url}/{book_info.sales_id}?salesItemId"
                           f"={book_info.sales_item_id}",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
                "nonce": nonce,
                "timestamp": str(timestamp),
                "signature": signature,
            },
            data={
                "key": cache_key,
                "isolationUser": 0,
                "value": value,
            },
            verify=False
        )
        if response.status_code == 200:
            return cache_key
        else:
            logger.error(book_info.name, response.status_code, response.content)
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
        print(e)
