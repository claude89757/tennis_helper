#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/10/18 13:23
@Author  : claudexie
@File    : tencent_docs_to_image.py
@Software: PyCharm
"""

import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from PIL import Image

from .publish_xiaohongshu import publish_image_and_text


def tencent_docs_to_image(image_path: str):
    """
    腾讯在线文档转化成截图
    """
    # 设置Firefox选项
    options = Options()
    options.add_argument("--headless")  # Ensure GUI is off

    # 指定geckodriver的路径
    # service = Service('/usr/local/bin/geckodriver')
    # 创建一个WebDriver实例
    # driver = webdriver.Firefox(service=service, options=options)
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)

    # 设置窗口大小
    driver.set_window_size(1080, 1920)  # 小红书推荐的尺寸

    # 打开临时HTML文件
    driver.get("https://docs.qq.com/sheet/DTkxyc09ZQmRuYWVk?tab=BB08J2&_t=1690340619074")

    # 等待JavaScript加载
    time.sleep(5)

    # 获取要截屏的元素
    element = driver.find_element(By.XPATH, "//div[@class='main-board']")
    print(element)

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


if __name__ == '__main__':
    image_path = "sheet_1.png"
    # 将Markdown转换为图片
    tencent_docs_to_image(image_path)

    # 获取当前脚本所在的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 拼接文件的绝对路径
    file_path = os.path.join(current_directory, image_path)

    # 打印文件的绝对路径
    print("文件的绝对路径：", file_path)

    publish_image_and_text(file_path, "深圳热门网球场动态", "深圳热门网球场动态")





