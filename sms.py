#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claudexie
@File    : send_text.py
@Software: PyCharm
"""
import os
import json

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

TENCENT_CLOUD_SECRET_ID = os.environ.get("TENCENT_CLOUD_SECRET_ID")
TENCENT_CLOUD_SECRET_KEY = os.environ.get("TENCENT_CLOUD_SECRET_KEY")


def send_sms_for_news(phone_num_list: list, param_list: list):
    """
    发生短信通知
    """
    sign_name = "网球场预定助手小程序"
    template_id = "1856675"
    try:
        # 必要步骤：
        # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
        # 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
        # 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
        # 以免泄露密钥对危及你的财产安全。
        # SecretId、SecretKey 查询: https://console.cloud.tencent.com/cam/capi
        cred = credential.Credential(TENCENT_CLOUD_SECRET_ID, TENCENT_CLOUD_SECRET_KEY)
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
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
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


# testing
if __name__ == '__main__':
    phone = "xxxxx"
    sms_res = send_sms_for_news(["xxxxx"], param_list=["08-03", "大沙河", "21:00", "20:00"])
    print(sms_res)
