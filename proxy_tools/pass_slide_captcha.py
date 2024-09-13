#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-09-13
@Author  : claude
@File    : pass_slide_captcha.py
@Software: PyCharm
"""

import os
import time
import random
import requests
import json
import base64

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


FILENAME = "isz_https_proxies_infos.json"


def generate_proxies():
    """
    获取待检查的代理列表
    """
    urls = [
        "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/isz_https_proxies.txt"
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


# 上传文件（相当于推送）
def upload_file_to_github(data_list: list):
    token = os.environ['GIT_TOKEN']
    repo = 'claude89757/free_https_proxies'
    url = f'https://api.github.com/repos/{repo}/contents/{FILENAME}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # 把data_list转换成content
    content = json.dumps(data_list)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    data = {
        'message': f'Update proxy list by scf',
        'content': encoded_content,
        'sha': get_file_sha(url, headers)  # You need to get the SHA if you're updating an existing file
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print(F"File uploaded successfully, total {len(data_list)} proxies")
    else:
        print("Failed to upload file:", response.status_code, response.text)


def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None


class TwitterWatcher:
    def __init__(self, timeout=10, headless: bool = True):
        self.driver_path = "/usr/local/bin/chromedriver"
        self.timeout = timeout
        self.interaction_timeout = 10
        self.driver = None
        self.headless = headless

    def setup_driver(self, proxy=None):
        chrome_options = Options()
        chrome_options.add_argument("--lang=cn")
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # 定义多个 User-Agent 字符串
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]

        # 随机选择一个 User-Agent
        random_user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={random_user_agent}")

        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        # Check Selenium version
        selenium_version = selenium.__version__

        if selenium_version.startswith('3'):
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
        else:
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()

    def random_delay(self, min_delay=1, max_delay=3):
        time.sleep(random.uniform(min_delay, max_delay))

    def wait_for_element(self, by, value, timeout=None):
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def wait_for_url_change(self, current_url, timeout=None):
        timeout = timeout or self.timeout
        WebDriverWait(self.driver, timeout).until(EC.url_changes(current_url))

    def solve_slider_captcha(self):
        slider = self.wait_for_element(By.CLASS_NAME, "btn_slide")
        action_chains = ActionChains(self.driver)

        # 点击并按住滑块
        action_chains.click_and_hold(slider).perform()
        time.sleep(random.uniform(0.5, 1.0))  # 模拟人类按住滑块的时间

        # 模拟人类滑动的过程
        total_offset = 300  # 滑动的总距离
        current_offset = 0
        while current_offset < total_offset:
            move_by = random.randint(10, 30)  # 每次滑动的距离
            action_chains.move_by_offset(move_by, 0).perform()
            current_offset += move_by
            time.sleep(random.uniform(0.01, 0.03))  # 每次滑动后的短暂延迟

        # 释放滑块
        action_chains.release().perform()
        time.sleep(random.uniform(0.5, 1.0))  # 模拟人类释放后的时间

    def transfer_cookies(self):
        cookies = self.driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        return session

    def transfer_headers(self):
        headers = {
            'User-Agent': self.driver.execute_script("return navigator.userAgent;")
        }
        return headers


if __name__ == '__main__':
    """
    缓存各代理访问ISZ的方式
    """
    start_time = time.time()
    output_data = []
    proxy_list = generate_proxies()
    for server_and_port in proxy_list:
        print(f"Checking {server_and_port}")
        watcher = TwitterWatcher(headless=True)
        proxy = f"http://{server_and_port}"
        watcher.setup_driver(proxy=proxy)
        try:
            url = os.environ['ISZ_URL']
            watcher.driver.get(url)

            # 随机延迟模拟人类行为
            watcher.random_delay()

            # 等待页面加载完成
            watcher.wait_for_element(By.TAG_NAME, "body")

            if "签名错误,接口未签名" in str(watcher.driver.page_source):
                print(f"[1] processing directly...")
                # 无需滑块验证
                current_url = watcher.driver.current_url
                print(f"Current URL: {current_url}")
                output_data.append({
                    "proxy": server_and_port,
                    "type": "direct",
                    "target_url": current_url,
                })
            else:
                print(f"[2] processing by slider...")
                # 解决滑块验证
                watcher.solve_slider_captcha()

                # 等待页面加载完成
                WebDriverWait(watcher.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # 获取并打印当前的URL
                current_url = watcher.driver.current_url
                print(f"Current URL: {current_url}")

                # 使用requests通过代理请求current_url
                cookies = watcher.driver.get_cookies()
                session = requests.Session()
                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
                headers = {
                    'User-Agent': watcher.driver.execute_script("return navigator.userAgent;")
                }
                print(f"cookies: {cookies}")
                print(f"headers: {headers}")
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
                response = session.get(current_url, headers=headers, proxies=proxies)
                print(f"Response from {current_url}:")
                print(response.text)

                output_data.append({
                    "proxy": server_and_port,
                    "type": "by cookies",
                    "target_url": current_url,
                    "cookies": cookies,
                    "headers": headers,
                })

        except Exception as error:
            print(f"proxy {server_and_port} failed: {error}")
        finally:
            watcher.teardown_driver()
    upload_file_to_github(output_data)

    # 记录耗时
    cost_time = time.time() - start_time
    print(f"Total cost time：{cost_time} s")
