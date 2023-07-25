#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/4 15:24
@Author  : claude89757
@File    : update_docs.py
@Software: PyCharm
"""

import os
import time

from weda import get_today_active_rule_list
from weda import update_record_info_by_id

# 读取指定环境变量的值
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SIGN_KEY = os.environ.get("SIGN_KEY")


if __name__ == '__main__':
    # 指定文件夹路径
    folder_path = "./"
    # 列出文件夹中的所有文件
    file_names = os.listdir(folder_path)
    # 遍历每个文件并读取其内容
    for file_name in file_names:
        if "available_court" in file_name:
            court_name = file_name.split('_')[0]
            # 拼接文件路径
            file_path = os.path.join(folder_path, file_name)
            # 打开文件并读取内容
            with open(file_path, "r") as f:
                content = f.read()
            # 处理文件内容
            print(f"File {file_name}\n{content}")

            # 将文件内容按行分割
            lines = content.splitlines()

        else:
            # 其他文件不处理
            pass
