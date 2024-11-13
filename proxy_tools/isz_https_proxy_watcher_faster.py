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
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time


FILENAME = "isz_https_proxies.txt"


def generate_proxies():
    """
    获取待检查的代理列表
    """
    urls = [
        # "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/isz_https_proxies.txt",
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


# 添加配置类
class ProxyCheckerConfig:
    def __init__(self):
        self.initial_concurrency = 50  # 初始并发数
        self.max_concurrency = 100     # 最大并发数
        self.min_concurrency = 10      # 最小并发数
        self.success_threshold = 0.3    # 成功率阈值
        self.check_interval = 60       # 调整并发的时间间隔(秒)
        self.current_concurrency = self.initial_concurrency
        
        # 统计数据
        self.total_checked = 0
        self.success_count = 0
        self.last_adjust_time = time.time()

    def adjust_concurrency(self):
        """动态调整并发数"""
        current_time = time.time()
        if current_time - self.last_adjust_time < self.check_interval:
            return

        if self.total_checked == 0:
            return

        success_rate = self.success_count / self.total_checked
        
        if success_rate > self.success_threshold:
            # 成功率高，增加并发
            self.current_concurrency = min(
                self.current_concurrency + 10, 
                self.max_concurrency
            )
        else:
            # 成功率低，减少并发
            self.current_concurrency = max(
                self.current_concurrency - 5,
                self.min_concurrency
            )
            
        print(f"调整并发数到: {self.current_concurrency}, 成功率: {success_rate:.2%}")
        self.last_adjust_time = current_time
        self.total_checked = 0
        self.success_count = 0


# 修改检查代理的函数为异步版本
async def check_proxy_async(proxy_url, proxy_url_infos, session, config):
    """异步检查代理是否可用"""
    try:
        print(f"正在检查 {proxy_url}")
        target_url = 'https://wxsports.ydmap.cn/srv200/api/pub/basic/getConfig'
        
        async with session.get(
            target_url,
            proxy=f"http://{proxy_url}",
            timeout=aiohttp.ClientTimeout(total=3)
        ) as response:
            response_text = await response.text()
            
            config.total_checked += 1
            
            if response.status == 200 and ("html" in response_text or "签名错误" in response_text):
                print(f"[OK] {proxy_url} from {proxy_url_infos.get(proxy_url)}")
                config.success_count += 1
                return proxy_url
                
    except Exception as error:
        print(f"代理 {proxy_url} 检查失败: {str(error)}")
    
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


# 修改主任务函数
async def task_check_proxies_async():
    config = ProxyCheckerConfig()
    
    # 下载文件
    download_file()
    
    # 获取待检查的proxy列表
    proxies, proxy_url_infos = generate_proxies()
    print(f"开始检查 {len(proxies)} 个代理")
    
    available_proxies = []
    
    # 创建 aiohttp 会话
    async with aiohttp.ClientSession() as session:
        while proxies:
            # 动态调整并发数
            config.adjust_concurrency()
            
            # 取出当前批次要处理的代理
            batch_proxies = proxies[:config.current_concurrency]
            proxies = proxies[config.current_concurrency:]
            
            # 创建当前批次的任务
            tasks = [
                check_proxy_async(proxy, proxy_url_infos, session, config)
                for proxy in batch_proxies
            ]
            
            # 等待当前批次完成
            results = await asyncio.gather(*tasks)
            
            # 处理结果
            valid_proxies = [p for p in results if p]
            if valid_proxies:
                available_proxies.extend(valid_proxies)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{now} 可用代理数量: {len(available_proxies)}")
                
                # 更新文件
                update_proxy_file(FILENAME, available_proxies)
                # 上传到GitHub
                upload_file_to_github(FILENAME)

    print("检查完成")


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


# 修改主入口
if __name__ == '__main__':
    asyncio.run(task_check_proxies_async())
