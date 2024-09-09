#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/8 21:43
@Author  : claude
@File    : wx_watcher.py
@Software: PyCharm
"""
import requests
import json

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_url_md5_to_remote(md5__1182: str):
    api_url = 'http://43.156.239.164:5000/save_url_md5'
    headers = {'Content-Type': 'application/json'}
    data = {'md5__1182': md5__1182}

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，抛出HTTPError
        print(f"API call successful: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {"error": str(e)}


if __name__ == '__main__':
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='BH901V3R9E',
        appPackage='com.microsoft.emmx',  # 微信的包名
        appActivity='com.microsoft.ruby.Main',  # 微信的启动活动
        noReset=True,  # 不重置应用的状态
        fullReset=False,  # 不完全重置应用
        forceAppLaunch=True  # 强制重新启动应用

    )
    appium_server_url = 'http://localhost:4723'
    print('Loading driver...')
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    print('Driver loaded successfully.')

    # 访问指定的URL
    driver.get('https://isz.ydmap.cn/srv100352/api/pub/sport/venue/getVenueOrderList')

    new_url = WebDriverWait(driver, 10).\
        until(expected_conditions.presence_of_element_located((AppiumBy.ID, 'com.microsoft.emmx:id/url_bar'))).text
    print(f"new_url: {new_url}")
    new_md5 = str(new_url).split("=")[-1]

    # 等待页面加载完成并匹配包含特定文本的元素
    response_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//*[@class="android.widget.TextView" and contains(@text, "签名错误,接口未签名")]'))
    )
    # 获取元素的文本内容
    response_text = response_element.text
    print(f"response: {response_text}")

    # 同步到远程服务器上
    save_url_md5_to_remote(new_md5)

    # 关闭浏览器
    driver.quit()
