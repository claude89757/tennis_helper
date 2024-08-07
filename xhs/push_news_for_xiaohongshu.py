#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/10/18 13:23
@Author  : claude
@File    : tencent_docs_to_image.py
@Software: PyCharm
"""

import sys
import Config
import Cookie
import Init
import Create
import time
import os

from datetime import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def user_login():
    while Config.UserList:
        login_success_user_list = []
        for i, v in enumerate(Config.UserList):
            print(f"{i + 1}.{v}", end="\t")
            login_success_user_list.append(v)
        if login_success_user_list:
            Config.CurrentUser = Config.UserList[0]
            return
        else:
            # 手机号登录
            Config.login_status = True
            return


def login_successful():
    # 获取昵称
    print("尝试登录...")
    name_content = WebDriverWait(Config.Browser, 10, 0.2).until(
        lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    print(f"{name_content},登录成功!")
    Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
    Config.CurrentUser = name_content
    # 获取Cookie
    Cookie.get_new_cookie()
    Cookie.save_cookie()


def cookie_login():
    Cookie.set_cookie()
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    except TimeoutException:
        Config.login_status = True
        return
    login_successful()


def login():
    print("登录中...")
    Config.Browser.get("https://creator.xiaohongshu.com/login")
    if not Config.login_status:
        cookie_login()
        return
    # 访问登陆页面
    while True:
        phone = input("请输入手机号：")
        if len(phone) == 11:
            break
        print("手机号码不合法！")

    # 等待手机号输入框加载并可见
    print("等待手机号输入框加载并可见")
    phone_input = WebDriverWait(Config.Browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='手机号']")))
    phone_input.send_keys(phone)

    # 发送验证码
    print(" 发送验证码")
    send_code_button = WebDriverWait(Config.Browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='发送验证码']")))
    send_code_button.click()

    # 获取错误标签
    print("获取错误标签")
    error_span = 'return document.querySelector(".css-1qf7tqh").innerText'
    error = Config.Browser.execute_script(error_span)
    if error != "":
        print(error)
        return

    while True:
        # 输入验证码
        code = input("请输入验证码：")
        if len(code) == 6:
            break
        print("验证码不合法！")

    # 等待验证码输入框加载并可见
    code_input = WebDriverWait(Config.Browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='验证码']")))
    code_input.send_keys(code)

    # 登录
    login_button = WebDriverWait(Config.Browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1jgt0wa.css-kyhkf6.dyn")))
    Config.Browser.execute_script("arguments[0].click();", login_button)

    login_successful()


def switch_users():
    print("正在清除Cookie")
    Config.Browser.delete_all_cookies()
    # select_user()
    login()


def Quit():
    Cookie.save_cookie()
    print("Bye!")
    Config.Browser.quit()
    sys.exit(0)


def publish_image_and_text(path_images: str, title: str, describe: str):
    """
    发布图文内容
    """
    # 初始化程序
    print("正在初始化程序……")
    Init.init()
    # 缓存用户登录
    user_login()
    # 是否需要新登录
    login()

    if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish":
        print("getting: https://creator.xiaohongshu.com/publish/publish")
        Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")

    Create.create_image_and_text(path_images, title, describe)


def tencent_docs_to_image(image_path: str):
    """
    腾讯在线文档转化成截图
    """
    print("loading firefox driver ...")
    # 设置Firefox选项
    options = Options()
    options.add_argument("--headless")  # Ensure GUI is off
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'   # test for win11

    # 指定geckodriver的路径
    # service = Service('/usr/local/bin/geckodriver')
    service = Service(r'C:\Program Files\geckodirver\geckodriver.exe')  # test for win11
    # 创建一个WebDriver实例
    driver = webdriver.Firefox(service=service, options=options)

    # 设置窗口大小
    driver.set_window_size(1080, 1920)  # 小红书推荐的尺寸

    # 打开网站页面
    driver.get("https://docs.qq.com/sheet/DTkxyc09ZQmRuYWVk?tab=BB08J2")
    print("loading url...")
    time.sleep(10)
    element = driver.find_element(By.XPATH, "//div[@class='main-board']")
    print(f"element: {element}")
    element = driver.find_element(By.XPATH, "//div[@class='main-board']")

    # 元素截图
    element.screenshot('sheet.png')

    # 使用PIL库裁剪保存截图
    image = Image.open('sheet.png')
    cropped_image = image.crop((0, 0, 560, 780))
    cropped_image.save(image_path)

    # 关闭WebDriver实例
    driver.quit()

    # 删除临时文件
    os.remove('sheet.png')


# testing
if __name__ == '__main__':
    # 获取当前时间
    current_time = datetime.now()

    # 将时间格式化为字符串
    cur_time = current_time.strftime("%m-%d_%H:%M")

    # 获取当前脚本所在的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 拼接文件的绝对路径
    image_path = f"tennis_sheet.png"
    file_path = os.path.join(current_directory, image_path)

    # 打印文件的绝对路径
    print("文件的绝对路径：", file_path)

    msg = f"[test]笔记每小时自动发布\n【访问原文档, 请私信】\n #深圳网球#"

    publish_image_and_text(file_path, f"[test]深圳热门网球场动态", msg)
