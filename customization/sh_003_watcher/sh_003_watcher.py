#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/13 23:31
@Author  : claude89757
@File    : tennis_court_watcher.py
@Software: PyCharm
"""
import os
import json
import time
import datetime
import shelve
import requests
import random
import argparse

from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def send_sms_for_news(phone_num_list: list, param_list: list, template_id: str = '1856675'):
    """
    发生短信通知
    example: send_sms_for_news(["xxxxx"], param_list=["08-03", "大沙河", "21:00", "20:00"])
    """
    secret_id = os.environ.get("TENCENT_CLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENT_CLOUD_SECRET_KEY")
    sign_name = "网球场预定助手小程序"
    try:
        # 必要步骤：
        # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
        # 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
        # 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
        # 以免泄露密钥对危及你的财产安全。
        # SecretId、SecretKey 查询: https://console.cloud.tencent.com/cam/capi
        cred = credential.Credential(secret_id, secret_key)
        # cred = credential.Credential(
        #     os.environ.get(""),
        #     os.environ.get("")
        # )

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        # 如果需要指定proxy访问接口，可以按照如下方式初始化hp（无需要直接忽略）
        # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        # 实例化要请求产品(以sms为例)的client对象
        # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，支持的地域列表参考
        # https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
        # 属性可能是基本类型，也可能引用了另一个数据结构
        # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
        req = models.SendSmsRequest()

        # 基本类型的设置:
        # SDK采用的是指针风格指定参数，即使对于基本类型你也需要用指针来对参数赋值。
        # SDK提供对基本类型的指针引用封装函数
        # 帮助链接：
        # 短信控制台: https://console.cloud.tencent.com/smsv2
        # 腾讯云短信小助手: https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81

        # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
        # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
        req.SmsSdkAppId = "1400835675"
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
        # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
        req.SignName = sign_name
        # 模板 ID: 必须填写已审核通过的模板 ID
        # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template)
        # 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
        req.TemplateId = template_id
        # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
        req.TemplateParamSet = param_list
        # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不超过200个手机号
        req.PhoneNumberSet = phone_num_list
        # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = ""
        # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.ExtendCode = ""
        # 国内短信无需填写该项；国际/港澳台短信已申请独立 SenderId 需要填写该字段，默认使用公共 SenderId，无需填写该字段。
        # 注：月度使用量达到指定量级可申请独立 SenderId 使用，详情请联系
        # [腾讯云短信小助手](https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81)。
        req.SenderId = ""

        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)


def print_with_timestamp(*args, **kwargs):
    """
    打印函数带上当前时间戳
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print(timestamp, *args, **kwargs)


def merge_time_ranges(data: List[List[str]]) -> List[List[str]]:
    """
    将时间段合并
    Args:
        data: 包含多个时间段的列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '08:00'], ['07:00', '09:00'], ...]
    Returns:
        合并后的时间段列表，每个时间段由开始时间和结束时间组成，格式为[['07:00', '09:00'], ['09:00', '16:00'], ...]
    """
    if not data:
        return data
    else:
        pass
    print(f"merging {data}")
    # 将时间段转换为分钟数，并按照开始时间排序
    data_in_minutes = sorted([(int(start[:2]) * 60 + int(start[3:]), int(end[:2]) * 60 + int(end[3:]))
                              for start, end in data])

    # 合并重叠的时间段
    merged_data = []
    start, end = data_in_minutes[0]
    for i in range(1, len(data_in_minutes)):
        next_start, next_end = data_in_minutes[i]
        if next_start <= end:
            end = max(end, next_end)
        else:
            merged_data.append((start, end))
            start, end = next_start, next_end
    merged_data.append((start, end))

    # 将分钟数转换为时间段
    result = [[f'{start // 60:02d}:{start % 60:02d}', f'{end // 60:02d}:{end % 60:02d}'] for start, end in merged_data]
    print(f"merged {result}")
    return result


def get_free_tennis_court_data(venue_id: str, book_time: str, proxy_list: list = None, ok_proxy_list: list = None):
    """
    查询空闲场地信息
    """
    success_proxy_list = []
    url = "https://jsapp.jussyun.com/jiushi-core/venue/getVenueGround"
    headers = {
        "Host": "jsapp.jussyun.com",
        "os_type": "wechat_mini",
        "fullMobile": "18688539560",
        "gw_channel": "api",
        "app_id": "0ff444f417de34c1352af3b3ffc30348",
        "js_sign": "OWFhMmNmOTFjZjJlZjE3NjRjMzNhMmMyZjQ0MjgwYjY=",
        "os_version": "Mac OS X 15.0.1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.9(0x13080911) XWEB/1227",
        "Content-Type": "application/json",
        "xweb_xhr": "1",
        "device_type": "MacBookPro18,1",
        "token": "kLzLiLeGCWua6C0XKWvPaN3POeYoQSJWef6CoYk1Bux2QOEUiJd16p3Ihv2R9SEQ+qaudBZUe7LoNiuEcUmuMpTRY7Oi1upzTi9JOpaSNya5nEVFa3tBo7IvJuV5W9rn0U6O9Pcp0duhEvW0IcYU/gTYFD3qNt5l0P09NNZ0NW8",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxbd4ec54a9e9ce6dd/115/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cookie": "ssxmod_itna3=C50qzxBDRDuDcGCGCDyDA2D+hfmtDQFsD9COrOlxB++8IxDs0D6mxqeKDCgDjxWKQD=1q07De40kYxjKDADY5RQYD0+6hexD4GvDQaFD7p=wqaLjxA6+R7AGRYeK7A8UqODnqD8D/40iDC4IgiiPoGh5DbqGuRqDSQix7jYqdGh4KKrb36eTOYqI7IjbtuWWbw2IWhraapxKxD;"
    }
    data = {
        "venueId": venue_id,
        "bookTime": book_time
    }
    
    res = None
    if proxy_list or ok_proxy_list:
        all_proxy_list = ok_proxy_list + proxy_list if ok_proxy_list else proxy_list
        
        for proxy in all_proxy_list:
            try:
                if not proxy.startswith("http://") and not proxy.startswith("https://"):
                    proxy = "http://" + proxy
                proxies = {"https": proxy}
                response = requests.post(url, headers=headers, json=data, proxies=proxies, verify=False, timeout=2)
                if response.status_code == 200:
                    success_proxy_list.append(proxy)
                    res = response.json()
                    break
                else:
                    time.sleep(1)
            except Exception:
                continue
    else:
        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            res = response.json()
        else:
            raise Exception(str(response.text))

    if res and res["rtnCode"] == "10000":
        print("请求成功:", res["rtnMessage"])
        status_list = res["data"]["statusList"]
        free_time_list = []
        for time_slot in status_list:
            start_time = datetime.datetime.fromtimestamp(int(time_slot["startTime"]) / 1000).strftime("%H:%M")
            end_time = datetime.datetime.fromtimestamp(int(time_slot["endTime"]) / 1000).strftime("%H:%M")
            for block in time_slot["blockModel"]:
                if block["status"] == "0":  # 0 表示可预订
                    free_time_list.append({
                        "groundName": block["groundName"],
                        "startTime": start_time,
                        "endTime": end_time,
                        "price": block["price"]
                    })
        return free_time_list, success_proxy_list
    else:
        raise Exception("未知异常")


# TESTING
if __name__ == '__main__':
    """
    云函数入口
    :param event:
    :param context:
    :return:
    """
    if datetime.time(0, 0) <= datetime.datetime.now().time() < datetime.time(8, 0):
        print("每天0点-8点不巡检")
        exit()
    else:
        pass
    # 获取脚本运行的时间
    start_min_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    end_min_time = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:00")

    # 网球场守望者开始时间
    run_start_time = time.time()
    print_with_timestamp("start to check...")

    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--phone', type=int, help='phone num', required=False)
    # 解析命令行参数
    args = parser.parse_args()
    # 检查必需的参数是否输入
    if not all([args.phone]):
        parser.print_help()
        exit()
    else:
        # 处理命令行参数
        print(args.phone)

    # 获取公网HTTPS代理列表
    url = "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/https_proxies.txt"
    response = requests.get(url)
    text = response.text.strip()
    lines = text.split("\n")
    proxy_list = [line.strip() for line in lines]
    random.shuffle(proxy_list)  # 每次都打乱下
    print(f"Loaded {len(proxy_list)} proxies from {url}")
    proxy_list = []  # 测试阶段，先不使用代理

    # 查询空闲的球场信息
    up_for_send_data_list = []
    ok_proxy_list = []
    venue_id = "20"  # 假设这是卢湾中心的venue_id
    for index in range(0, 7):
        book_time = str(int((datetime.datetime.now() + datetime.timedelta(days=index)).timestamp() * 1000))
        inform_date = (datetime.datetime.now() + datetime.timedelta(days=index)).strftime('%m-%d')
        data_list, ok_proxy_list = get_free_tennis_court_data(venue_id, book_time, proxy_list=proxy_list, ok_proxy_list=ok_proxy_list)
        time.sleep(1)
        if data_list:
            for data in data_list:
                court_type = "室内" if "室内" in data["groundName"] else "室外"
                hour_num = int(data["startTime"].split(":")[0])
                if (court_type == "室内" and 8 <= hour_num <= 21) or (court_type == "室外" and 18 <= hour_num <= 21):
                    up_for_send_data_list.append({
                        "date": inform_date,
                        "court_name": f"卢湾{court_type}",
                        "start_time": data["startTime"],
                        "end_time": data["endTime"],
                        "price": data["price"]
                    })

    up_for_send_sms_list = []
    if up_for_send_data_list:
        # 打开本地文件缓存，用于缓存标记已经发送过的短信
        cache = shelve.open(f'/tmp/sh_001_cache')
        for up_for_send_data in up_for_send_data_list:
            date = up_for_send_data['date']
            court_name = up_for_send_data['court_name']
            start_time = up_for_send_data['start_time']
            end_time = up_for_send_data['end_time']
            price = up_for_send_data['price']
            cache_key = f"{court_name}_{date}_{start_time}"
            if cache_key in cache:
                # 已通知过
                pass
            else:
                # 加入待发送短信队里
                up_for_send_sms_list.append({"phone": str(args.phone),
                                             "date": date,
                                             "court_name": court_name,
                                             "start_time": start_time,
                                             "end_time": end_time
                                             })
                # 更新本地文件缓存
                cache[cache_key] = 1
        # 关闭本地文件缓存
        cache.close()

        # 发送短信
        for sms_info in up_for_send_sms_list:
            print(f"sending {sms_info}...")
            phone = sms_info['phone']
            date = sms_info['date']
            court_name = sms_info['court_name']
            start_time = sms_info['start_time']
            end_time = sms_info['end_time']
            sms_res = send_sms_for_news([phone], [date, court_name, start_time, end_time])
            print(sms_res)
            if "send success" in str(sms_res):
                print_with_timestamp("短信发送成功")
            else:
                print_with_timestamp("短信发送失败")
            time.sleep(5)
    else:
        print_with_timestamp(F"无需要通知的场地信息")

    # 计算整体运行耗时
    run_end_time = time.time()
    execution_time = run_end_time - run_start_time
    print_with_timestamp(f"Total cost time：{execution_time} s")

    # # 缓存记录到日志
    # if up_for_send_data_list or up_for_send_sms_list:
    #     status = 1
    # else:
    #     status = 0
    # output_data = {"start_time": start_min_time, "end_time": end_min_time,
    #                "status": status, "place_name": "卢湾中心", "city": "上海",
    #                "up_for_send_num": len(up_for_send_data_list), "send_num": len(up_for_send_sms_list)}
    # print(F"[GRAFANA_DATA]@{json.dumps(output_data)}")


