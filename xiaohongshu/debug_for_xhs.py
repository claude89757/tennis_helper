#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# 如果Geckodriver不在系统路径中，需要指定路径
# service = Service(executable_path='/usr/local/bin/geckodriver')

# 创建Firefox WebDriver实例
driver = webdriver.Firefox()  # 如果需要指定service，加入参数：service=service

try:
    # 访问小红书创建者平台登录页面
    driver.get("https://creator.xiaohongshu.com/login")

    # 打印网页标题
    print("Title: ", driver.title)

finally:
    # 关闭浏览器
    driver.quit()