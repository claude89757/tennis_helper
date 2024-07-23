#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/23 10:41
@Author  : claudexie
@File    : get_szw_cookie.py
@Software: PyCharm
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import json

def get_cookies(url):
    # 设置Firefox无头浏览器选项
    options = Options()
    options.headless = True

    # 指定geckodriver的路径
    service = Service('/usr/local/bin/geckodriver')

    # 创建一个WebDriver实例
    driver = webdriver.Firefox(service=service, options=options)

    # 访问网站
    driver.get(url)

    # 等待一段时间，确保页面加载完成
    time.sleep(5)

    # 提取Cookie
    cookies = driver.get_cookies()
    driver.quit()

    # 将Cookie保存到文件
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    print("Cookies saved to cookies.json")

if __name__ == "__main__":
    get_cookies("https://program.springcocoon.com")
