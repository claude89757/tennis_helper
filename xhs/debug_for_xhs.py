#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

print("loading firefox driver ...")
# 设置Firefox选项
options = Options()
options.add_argument("--headless")  # Ensure GUI is off

# 指定geckodriver的路径
service = Service('/usr/local/bin/geckodriver')
# 创建一个WebDriver实例
driver = webdriver.Firefox(service=service, options=options)

try:
    # 访问小红书创建者平台登录页面
    driver.get("https://creator.xiaohongshu.com/login")

    # 打印网页标题
    print("Title: ", driver.title)

finally:
    # 关闭浏览器
    driver.quit()