#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/14 15:04
@Author  : claude89757
@File    : proxy_watcher.py
@Software: PyCharm
"""
import requests
import concurrent.futures

from datetime import datetime


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
    return proxies


def check_proxy(proxy_url):
    """
    检查代理是否可用
    """
    try:
        # 检查HTTPS代理
        response = requests.get("https://baidu.ydmap.cn/", proxies={"https": proxy_url}, timeout=5)
        if response.status_code == 200:
            print(f"HTTPS Proxy {proxy_url} is working")
            return proxy_url
    except:
        pass
    try:
        # 检查HTTPS代理
        response = requests.get("https://baidu.ydmap.cn/", proxies={"https": "https://" + proxy_url}, timeout=5)
        if response.status_code == 200:
            print(f"HTTPS Proxy https://{proxy_url} is working")
            return "https://" + proxy_url
    except:
        pass
    return None


def task_check_proxies():
    """
    并发检查代理
    """
    proxies = generate_proxies()
    available_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result is not None:
                    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    proxy_with_timestamp = {"proxy": result, "timestamp": timestamp}
                    available_proxies.append(proxy_with_timestamp)
                    print(f"available_proxies: {len(available_proxies)}")
            except Exception as exc:
                print(f"{proxy} generated an exception: {exc}")


if __name__ == '__main__':
    # 每天0点-7点不巡检，其他时间巡检
    pass
