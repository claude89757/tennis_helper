#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-7-20 02:35:46
@Author  : claude89757
@File    : https_proxy_watcher.py
@Software: PyCharm
"""
import os
import requests
import datetime
import random
import base64


FILENAME = "isz_https_proxies.txt"


def generate_proxies():
    """
    获取待检查的代理列表
    """
    urls = [
        "https://raw.githubusercontent.com/parserpp/ip_ports/refs/heads/main/proxyinfo.txt",
        "https://github.com/roosterkid/openproxylist/raw/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/yoannchb-pro/https-proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    ]
    proxies = []

    proxy_url_infos = {}
    for url in urls:
        print(f"getting proxy list for {url}")
        response = requests.get(url)
        # 将文本内容按行分割，并去除每行两端的空格
        text = response.text.strip()
        lines = text.split("\n")
        lines = [line.strip() for line in lines]
        proxies.extend(lines)
        print(f"Loaded {len(lines)} proxies from {url}")
        for line in lines:
            proxy_url_infos[line] = url
    print(f"Total {len(proxies)} proxies loaded")
    random.shuffle(proxies)
    return proxies, proxy_url_infos


def check_proxy(proxy_url, proxy_url_infos):
    """
    检查代理是否可用
    """
    try:
        print(f"Checking {proxy_url}")
        # target_url = 'https://isz.ydmap.cn/srv100352/api/pub/sport/venue/getVenueOrderList'
        #
        # # 构建请求头
        # headers = {
        #     'visitor-id': 'test',
        # }

        target_url = 'https://isz.ydmap.cn/srv100352/api/pub/sport/venue/getVenueOrderList'
        params = {
            'salesItemId': '100341',
            'curDate': '1726588800000',
            'venueGroupId': '',
            't': '1726638536209',
            'timestamp__1762': 'test'
        }
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'access-token': 'test',
            'cookie': 'test',
            'cross-token': '',
            'entry-tag': '',
            'nonce': 'test',
            'openid-token': '',
            'priority': 'u=1, i',
            'referer': 'https://wxsports.ydmap.cn/booking/schedule/101332?salesItemId=100341',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'signature': 'test',
            'tab-id': 'ydmap_fb2fd7837857e118f6d3861c83d449fc',
            'timestamp': '1726638536213',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/129.0.0.0 Safari/537.36',
            'visitor-id': 'test',
            'x-requested-with': 'XMLHttpRequest'
        }

        # 使用代理发送请求
        proxies = {
            "http": f"http://{proxy_url}",
            "https": f"http://{proxy_url}"
        }

        response = requests.get(target_url, headers=headers, params=params, proxies=proxies, timeout=3)
        print(str(response.text)[:100])

        if response.status_code == 200 and "html" in str(response.text):
            print(f"[OK]  {proxy_url}, from {proxy_url_infos.get(proxy_url)}")
            return proxy_url

        if response.status_code == 200 and response.json().get('code') == -1 and "签名错误" in response.json().get('msg',
                                                                                                               ''):
            print(f"[OK] {proxy_url} from {proxy_url_infos.get(proxy_url)}")
            return proxy_url
    except Exception as error:
        print(str(error).split()[0])
    return None


def update_proxy_file(filename, available_proxies):
    # 读取现有的代理列表
    try:
        with open(filename, "r") as file:
            existing_proxies = file.readlines()
    except FileNotFoundError:
        existing_proxies = ""

    # 清理现有代理列表中的换行符
    existing_proxies = [proxy.strip() for proxy in existing_proxies]

    # 过滤出不在文件中的新代理
    new_proxies = [proxy for proxy in available_proxies if proxy not in existing_proxies]

    # 如果有新的有效代理，追加到文件
    if new_proxies:
        with open(filename, "a") as file:
            for proxy in new_proxies:
                file.write(proxy + "\n")

    # 检查文件行数，如果超过100行，则删除前50行
    with open(filename, "r") as file:
        lines = file.readlines()

    if len(lines) > 400:
        with open(filename, "w") as file:
            file.writelines(lines[200:])  # 保留从第200行到最后的行


def task_check_proxies():
    # 下载文件
    download_file()
    # 获取待检查的proxy列表
    proxies, proxy_url_infos = generate_proxies()
    print(f"start checking {len(proxies)} proxies")
    available_proxies = []
    for proxy in proxies:
        # print(f"checking {proxy}")
        if check_proxy(proxy, proxy_url_infos):
            available_proxies.append(proxy)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{now} Available proxies: {len(available_proxies)}")
            # 更新文件
            update_proxy_file(FILENAME, available_proxies)
            # 上传到GIT
            upload_file_to_github(FILENAME)
        else:
            pass
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
    with open(FILENAME, 'rb') as file:
        content = file.read()
    data = {
        'message': f'Update proxy list by scf',
        'content': base64.b64encode(content).decode('utf-8'),
        'sha': get_file_sha(url, headers)  # You need to get the SHA if you're updating an existing file
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file:", response.status_code, response.text)


def download_file():
    """
    从指定的 URL 下载文件并保存到 /tmp 目录下，如果存在同名文件则覆盖。
    """
    # 完整的文件路径
    try:
        # 发送 GET 请求
        url = 'https://raw.githubusercontent.com/claude89757/free_https_proxies/main/free_https_proxies.txt'
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功，否则抛出异常

        # 写入文件
        with open(FILENAME, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {FILENAME}")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")


def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None


if __name__ == '__main__':
    task_check_proxies()
