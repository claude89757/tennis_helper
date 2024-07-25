#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-7-20 02:35:46
@Author  : claude89757
@File    : https_proxy_watcher.py
@Software: PyCharm
"""
import os
import json
import requests
import datetime
import random
import base64


FILENAME = "free_https_proxies.txt"


def generate_proxies():
    """
    获取待检查的代理列表
    """
    urls = [
        "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt",
        "https://github.com/roosterkid/openproxylist/raw/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/yoannchb-pro/https-proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    ]
    proxies = []

    for url in urls:
        print(f"getting proxy list for {url}")
        response = requests.get(url)
        # 将文本内容按行分割，并去除每行两端的空格
        text = response.text.strip()
        lines = text.split("\n")
        lines = [line.strip() for line in lines]
        proxies.extend(lines)
        print(f"Loaded {len(lines)} proxies from {url}")
    print(f"Total {len(proxies)} proxies loaded")
    random.shuffle(proxies)
    return proxies


def check_proxy(proxy_url):
    """
    检查代理是否可用
    """
    try:
        # 确保代理 URL 包含协议方案(requests==2.25.1版本才需要！！)
        if not proxy_url.startswith("http://") and not proxy_url.startswith("https://"):
            proxy_url = "http://" + proxy_url  # 假设代理支持 HTTP，也可以根据实际情况选择 https://

        response = requests.get("https://www.baidu.com/", proxies={"https": proxy_url}, timeout=2)
        if response.status_code == 200:
            print(f"HTTPS Proxy {proxy_url} is working")
            return proxy_url
    except:
        pass
    return None


def update_proxy_file(filename, available_proxies):
    # 读取现有的代理列表
    try:
        with open(filename, "r") as file:
            existing_proxies = file.readlines()
    except FileNotFoundError:
        existing_proxies = []

    # 清理现有代理列表中的换行符
    existing_proxies = [proxy.strip() for proxy in existing_proxies]

    # 过滤出不在文件中的新代理
    new_proxies = [proxy for proxy in available_proxies if proxy + "\n" not in existing_proxies]

    # 如果有新的有效代理，追加到文件
    if new_proxies:
        with open(filename, "a") as file:
            for proxy in new_proxies:
                file.write(proxy + "\n")

    # 检查文件行数，如果超过100行，则删除前50行
    with open(filename, "r") as file:
        lines = file.readlines()

    if len(lines) > 100:
        with open(filename, "w") as file:
            file.writelines(lines[50:])  # 保留从第51行到最后的行


def task_check_proxies():
    # 下载文件
    download_file()
    filename = f"/tmp/{FILENAME}"
    # 获取待检查的proxy列表
    proxies = generate_proxies()
    print(f"start checking {len(proxies)} proxies")
    available_proxies = []
    for proxy in proxies:
        # print(f"checking {proxy}")
        if check_proxy(proxy):
            available_proxies.append(proxy)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{now} Available proxies: {len(available_proxies)}")
            # 更新文件
            update_proxy_file(filename, available_proxies)
            # 上传到GIT
            upload_file_to_github(filename)
        else:
            pass
        if len(available_proxies) >= 5:
            break
        else:
            continue
    print("check end.")


# 上传文件（相当于推送）
def upload_file_to_github(filename):
    token = os.environ['GIT_TOKEN']
    repo = 'claude89757/free_https_proxies'
    url = f'https://api.github.com/repos/{repo}/contents/{FILENAME}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    with open(f"/tmp/{FILENAME}", 'rb') as file:
        content = file.read()
    data = {
        'message': f'Update proxy list by scf',
        'content': base64.b64encode(content).decode('utf-8'),
        'sha': get_file_sha(url, headers)  # You need to get the SHA if you're updating an existing file
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file:", response.status_code, response.text)


def download_file():
    """
    从指定的 URL 下载文件并保存到 /tmp 目录下，如果存在同名文件则覆盖。
    """
    # 完整的文件路径
    full_path = f"/tmp/{FILENAME}"
    try:
        # 发送 GET 请求
        url = 'https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt'
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功，否则抛出异常

        # 写入文件
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {full_path}")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")


def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None


def main_handler(event, context):
    """
    云函数入口
    :param event:
    :param context:
    :return:
    """
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))

    # 执行任务
    task_check_proxies()

    return "success"


if __name__ == '__main__':
    task_check_proxies()
