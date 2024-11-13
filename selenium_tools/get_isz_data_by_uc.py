#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024-09-13
@Author  : claude
@File    : get_data_by_chrome.py
@Software: PyCharm
"""

import os
import re
import time
import random
import requests
import json
import base64
import datetime
import argparse
import concurrent.futures
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

FILENAME = "isz_data_infos.json"
COOKIES_FILE = 'cookies.json'
HEADERS_FILE = 'headers.json'


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
        response = requests.get(url, timeout=10)
        text = response.text.strip()
        lines = text.split("\n")
        lines = [line.strip() for line in lines]
        proxies.extend(lines)
        print(f"Loaded {len(lines)} proxies from {url}")
    print(f"Total {len(proxies)} proxies loaded")
    random.shuffle(proxies)
    return proxies


def upload_file_to_github(input_data):
    token = os.environ.get('GIT_TOKEN', "")
    repo = 'claude89757/tennis_data'
    url = f'https://api.github.com/repos/{repo}/contents/{FILENAME}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    content = json.dumps(input_data)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    data = {
        'message': f'Update proxy list by scf',
        'content': encoded_content,
        'sha': get_file_sha(url, headers)
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"File uploaded successfully, total {len(input_data)} data")
    else:
        print("Failed to upload file:", response.status_code, response.text)


def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None


class IszWatcher:
    def __init__(self, timeout=10, headless: bool = True):
        self.timeout = timeout
        self.interaction_timeout = 10
        self.driver = None
        self.headless = headless
   
    def setup_driver(self, proxy=None):
        """
        初始化浏览器，使用undetected-chromedriver来规避检测
        自动适配当前Chrome版本
        """
        print("开始初始化Chrome驱动...")
        
        # 初始化Chrome选项
        chrome_options = uc.ChromeOptions()
        print("Chrome选项初始化完成")
        
        # 基础设置
        if not self.headless:
            chrome_options.add_argument("--start-maximized")
            print("设置为可视化模式")
        else:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            print("设置为无头模式，窗口大小: 1920x1080")
        
        # 代理设置
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
            print(f"设置代理服务器: {proxy}")
        else:
            print("未使用代理")

        # 获取当前系统的Chrome版本
        chrome_version = None
        try:
            if os.path.exists('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
                # macOS
                cmd = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version']
                chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            else:
                # Linux
                cmd = ['google-chrome', '--version']
                chrome_path = '/usr/bin/google-chrome'
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            version_output = result.stdout.strip()
            chrome_version = int(version_output.split()[2].split('.')[0])  # 提取主版本号
            print(f"检测到Chrome版本: {version_output}")
            
            # 设置Chrome二进制文件位置
            chrome_options.binary_location = chrome_path
            
        except Exception as e:
            print(f"获取Chrome版本失败: {str(e)}")
            print("将使用默认版本设置")

        print(f"尝试创建Chrome {chrome_version if chrome_version else '默认'}版本驱动...")
        try:
            self.driver = uc.Chrome(
                options=chrome_options,
                version_main=chrome_version,  # 使用检测到的版本号
                driver_executable_path=None  # 让undetected_chromedriver自动管理驱动
            )
            print("Chrome驱动创建成功！")
            print(f"Chrome版本: {self.driver.capabilities['browserVersion']}")
            print(f"ChromeDriver版本: {self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}")
        except Exception as e:
            print("=" * 50)
            print(f"创建Chrome驱动失败")
            print(f"错误信息: {str(e)}")
            print(f"请确保:")
            print("1. 已正确安装Chrome浏览器")
            print("2. 系统环境变量正确配置")
            print("3. 网络连接正常")
            print("=" * 50)
            raise Exception("Chrome驱动创建失败，请检查Chrome安装和系统配置")
        
        # 添加随机延迟
        delay = random.uniform(1, 3)
        print(f"添加随机延迟: {delay:.2f}秒")
        time.sleep(delay)
        print("Chrome驱动初始化完成！")

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
        time.sleep(random.uniform(0.5, 1.0))

        # 模拟人类滑动
        total_offset = 300
        current_offset = 0
        while current_offset < total_offset:
            move_by = random.randint(10, 30)
            action_chains.move_by_offset(move_by, 0).perform()
            current_offset += move_by
            time.sleep(random.uniform(0.01, 0.03))

        # 释放滑块
        action_chains.release().perform()
        time.sleep(random.uniform(0.5, 1.0))

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

def load_cookies_and_headers():
    if os.path.exists(COOKIES_FILE) and os.path.exists(HEADERS_FILE):
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
        with open(HEADERS_FILE, 'r') as f:
            headers = json.load(f)
        return cookies, headers
    return None, None


def save_cookies_and_headers(cookies, headers):
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f)
    with open(HEADERS_FILE, 'w') as f:
        json.dump(headers, f)


def print_with_timestamp(*args, **kwargs):
    """
    打印函数带上当前时间戳
    """
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    print(timestamp, *args, **kwargs)


def test_proxy(proxy):
    """
    使用curl命令测试代理是否可用
    """
    try:
        print(f"正在测试代理: {proxy}")
        target_url = 'https://wxsports.ydmap.cn/srv200/api/pub/basic/getConfig'

        # 使用curl命令发送请求
        curl_command = [
            'curl',
            '-x', f"http://{proxy}",
            '--max-time', '3',  # 设置超时时间为3秒
            '-s',  # 静默模式
            '-o', '-',  # 输出到标准输出
            '-w', '%{http_code}',  # 输出HTTP状态码
            target_url
        ]

        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        response_text = result.stdout[:-3]  # 去掉最后的状态码
        http_code = result.stdout[-3:]  # 获取状态码

        # print(f"响应内容预览: {response_text[:100]}")

        # 验证响应
        if http_code == '200' and "html" in response_text:
            print(f"[OK] 代理可用: {proxy}")
            return proxy

        if http_code == '200' and '"code":-1' in response_text and "签名错误" in response_text:
            print(f"[OK] 代理可用: {proxy}")
            return proxy
            
    except Exception as error:
        print(f"代理测试失败 {proxy}: {str(error)}")
    return None

def get_working_proxy():
    """
    获取一个可用的代理
    """
    proxies = generate_proxies()
    print(f"开始测试 {len(proxies)} 个代理...")
    
    # 使用线程池并发测试代理
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result:
                    return result
            except Exception as e:
                print(f"测试代理时发生错误 {proxy}: {str(e)}")
    
    return None

if __name__ == '__main__':
    """
    遍历查询多个网球场的信息，并缓存到 GitHub 上
    每5分钟执行一次，失败不会终止循环
    """
    while True:
        try:
            # 检查执行时间
            now = datetime.datetime.now()
            print_with_timestamp(f'开始新的任务循环 - {now}')
            
            # 在凌晨 0 点到 8 点之间跳过执行
            if datetime.time(0, 0) <= now.time() < datetime.time(8, 0):
                print_with_timestamp('当前是休息时间（0:00-8:00），跳过本次执行')
                time.sleep(300)  # 休息5分钟
                continue
                
            start_time = time.time()

            # 获取可用代理
            working_proxy = None
            try:
                working_proxy = get_working_proxy()
                if not working_proxy:
                    print("未找到可用代理，等待下次尝试")
                    time.sleep(300)  # 休息5分钟
                    continue
            except Exception as e:
                print(f"获取代理时出错: {str(e)}")
                time.sleep(300)  # 休息5分钟
                continue
            
            print(f"使用代理: {working_proxy}")
            watcher = None
            
            try:
                watcher = IszWatcher(headless=False)
                watcher.setup_driver(proxy=working_proxy)
                print("Driver setup complete.")

                # 开始浏览
                url = "https://wxsports.ydmap.cn/booking/schedule/101332?salesItemId=100341"
                watcher.driver.get(url)
                watcher.random_delay(min_delay=1, max_delay=5)

                watcher.wait_for_element(By.TAG_NAME, "body", timeout=10)
                cookies, headers = load_cookies_and_headers()
                if cookies and headers:
                    watcher.driver.get(url)
                    for cookie in cookies:
                        watcher.driver.add_cookie(cookie)
                    watcher.driver.get(url)
                    watcher.driver.refresh()
                    watcher.random_delay()
                    print(f"使用缓存的 cookies 和 headers 访问页面。")
                else:
                    watcher.driver.get(url)
                    print(f"没有找到缓存，直接访问页面。")

                watcher.random_delay(min_delay=5, max_delay=10)

                watcher.wait_for_element(By.TAG_NAME, "body", timeout=15)
                if "网球" in str(watcher.driver.page_source):
                    print(f"[1] Processing directly...")
                    current_url = watcher.driver.current_url
                    print(f"Current URL: {current_url}")
                elif "验证" in str(watcher.driver.page_source):
                    print(f"[2] Processing by solving slider captcha...")
                    access_ok = False
                    for index in range(3):
                        print(f"Try {index} time>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        watcher.random_delay()
                        watcher.solve_slider_captcha()
                        WebDriverWait(watcher.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        watcher.random_delay(min_delay=3, max_delay=10)
                        if "网球" in str(watcher.driver.page_source):
                            cookies = watcher.driver.get_cookies()
                            headers = {
                                'User-Agent': watcher.driver.execute_script("return navigator.userAgent;")
                            }
                            print(f"cookies: {cookies}")
                            print(f"headers: {headers}")
                            save_cookies_and_headers(cookies, headers)
                            for cookie in cookies:
                                watcher.driver.add_cookie(cookie)
                            watcher.driver.get(url)
                            access_ok = True
                            break
                        else:
                            print(f"Failed, try again...")

                    if access_ok:
                        pass
                    else:
                        print(f"Failed to solve slider captcha")
                        screenshot_path = 'screenshot.png'
                        watcher.driver.save_screenshot(screenshot_path)
                        page_source = watcher.driver.page_source
                        with open("page_source.html", "w", encoding='utf-8') as f:
                            f.write(page_source)
                        time.sleep(10)
                        raise Exception("自动化验证失败")
                else:
                    current_url = watcher.driver.current_url
                    print(f"Current URL: {current_url}")
                    screenshot_path = 'screenshot.png'
                    watcher.driver.save_screenshot(screenshot_path)
                    page_source = watcher.driver.page_source
                    with open("page_source.html", "w", encoding='utf-8') as f:
                        f.write(page_source)
                    time.sleep(10)
                    raise Exception(f"未知错误?")
                print(f"=====Access Success=====")

                url_infos = {
                    "香蜜体育": "https://wxsports.ydmap.cn/booking/schedule/101332?salesItemId=100341",
                    "莲花体育": "https://wxsports.ydmap.cn/booking/schedule/101335?salesItemId=100347",
                    "黄木岗": "https://wxsports.ydmap.cn/booking/schedule/101333?salesItemId=100344",
                    # "华侨城": "https://wxsports.ydmap.cn/booking/schedule/105143?salesItemId=105347",
                    # "简上": "https://wxsports.ydmap.cn/booking/schedule/103909?salesItemId=102913",
                }
                output_data = {}
                for place_name, url in url_infos.items():
                    place_data = {"url": url, "court_infos": {}}
                    print(f"Checking {place_name} {url}")
                    try:
                        watcher.driver.get(url)
                        watcher.random_delay(min_delay=1, max_delay=10)

                        watcher.wait_for_element(By.TAG_NAME, "body", timeout=5)

                        if "网球" in str(watcher.driver.page_source):
                            print(f"[1] Processing directly...")

                            page_source = watcher.driver.page_source

                            date_slider = WebDriverWait(watcher.driver, 10).\
                                until(EC.presence_of_element_located((By.CLASS_NAME, 'slider-box-datetime')))
                            date_elements = date_slider.find_elements(By.CLASS_NAME, 'new-datetime')
                            index = 0
                            for date_element in date_elements:
                                date_element.click()
                                watcher.random_delay(min_delay=2, max_delay=6)

                                date_text = date_element.find_element(By.CLASS_NAME, 'datetime').text
                                week_text = date_element.find_element(By.CLASS_NAME, 'week').text
                                print(f"Processing date: {date_text} {week_text}")

                                time_pattern = re.compile(r'\d{2}:\d{2}-\d{2}:\d{2}')
                                price_pattern = re.compile(r'\d+(?:\.\d+)?元')

                                page_source = watcher.driver.page_source

                                soup = BeautifulSoup(page_source, 'html.parser')

                                schedule_table_div = soup.find('div', class_='schedule-table text-center')

                                if schedule_table_div:
                                    tables = schedule_table_div.find_all('table')

                                    if len(tables) >= 2:
                                        header_table = tables[0]
                                        body_table = tables[1]
                                    else:
                                        print_with_timestamp(f"未找到足够的table元素")
                                        continue
                                else:
                                    print_with_timestamp(f"未找到'schedule-table text-center'的DIV")
                                    continue

                                venue_names = []
                                header_row = header_table.find('thead').find('tr')
                                header_cells = header_row.find_all('th')
                                for cell in header_cells:
                                    venue_name = cell.get_text(strip=True)
                                    if venue_name:
                                        venue_names.append(venue_name)

                                venue_times = {venue: [] for venue in venue_names}

                                def expand_cell(row_index, col_index, rowspan, colspan):
                                    for i in range(rowspan):
                                        for j in range(colspan):
                                            key = (row_index + i, col_index + j)
                                            occupied_cells.add(key)

                                def get_standard_status_class(body_rows):
                                    """
                                    分析找出最常用的表示"已预订"状态的class
                                    """
                                    span_class_status_infos = {}    

                                    for row in body_rows:
                                        first_cell = row.find(['td', 'th'])
                                        if not first_cell:
                                            continue
                                        
                                        # 获取时间信息
                                        div = first_cell.find('div')
                                        if not div:
                                            continue
                                        
                                        time_text = div.get_text(strip=True).split()[0]
                                        if not time_text or ':' not in time_text:
                                            continue

                                        # 分析该行所有单元格中的span
                                        cells = row.find_all(['td', 'th'])
                                        for cell in cells:
                                            spans = cell.find_all('span')
                                            for span in spans:
                                                # print(f"span: {span}")
                                                class_name = span.get('class', [''])[0]
                                                if not class_name:
                                                    continue
                                                span_text = span.get_text(strip=True)
                                                
                                                class_name_and_text = f"{class_name}|{span_text}"

                                                span_class_status_infos[class_name_and_text] = span_class_status_infos.get(class_name_and_text, 0) + 1
                                
                                    # print(f"span_class_status_infos: {sorted(span_class_status_infos.items(), key=lambda x: x[1], reverse=True)}")                                         
                                    class_name_and_text  = max(span_class_status_infos.items(), key=lambda x: x[1])[0]
                                    # print(f"class_name_and_text: {class_name_and_text}")
                                    class_name = class_name_and_text.split('|')[0]
                                    return class_name
                                 
                                if body_table:
                                    tbody = body_table.find('tbody')
                                    if tbody:
                                        body_rows = tbody.find_all('tr')
                                    else:
                                        body_rows = body_table.find_all('tr')
                                    
                                    # 获取标准状态class
                                    standard_status_class = get_standard_status_class(body_rows)
                                    print(f"standard_status_class: {standard_status_class}")
                                    
                                    num_cols = len(venue_names)
                                    occupied_cells = set()
                                    
                                    for row_index, row in enumerate(body_rows):
                                        col_index = 0
                                        cells = row.find_all(['td', 'th'])
                                        cell_index = 0
                                        
                                        while col_index < num_cols and cell_index < len(cells):
                                            cell = cells[cell_index]
                                            while (row_index, col_index) in occupied_cells:
                                                col_index += 1
                                                
                                            rowspan = int(cell.get('rowspan', 1))
                                            colspan = int(cell.get('colspan', 1))
                                            
                                            if col_index < num_cols:
                                                venue = venue_names[col_index]
                                                div_in_cell = cell.find('div')
                                                if div_in_cell:
                                                    # 获取时间信息
                                                    full_text = div_in_cell.get_text(separator=',', strip=False)
                                                    time_matches = time_pattern.findall(full_text)
                                                    time_slot = '-'.join(time_matches) if time_matches else ''
                                                    
                                                    # 获取真实状态
                                                    show_status = "?"
                                                    spans = div_in_cell.find_all('span')
                                                    for span in spans:
                                                        if span.get('class') and standard_status_class in span.get('class'):
                                                            span_text = span.get_text(strip=True)
                                                            show_status = span_text
                                                    if "元" in show_status:
                                                        real_status = "可预订"
                                                    else:
                                                        real_status = "已预定"
                                                    # 获取原始状态文本
                                                    temp_text = time_pattern.sub('', full_text)
                                                    raw_status = temp_text.strip()
                                                    
                                                    venue_times[venue].append({
                                                        'time': time_slot,
                                                        'status': real_status,
                                                        'show_status': show_status,                                                  
                                                        'raw_statut': raw_status,
                                                    })
                                                    
                                            expand_cell(row_index, col_index, rowspan, colspan)
                                            col_index += colspan
                                            cell_index += 1
                                else:
                                    print_with_timestamp(f"未找到body_table")
                                    raise Exception("未找到body_table")
                                place_data['court_infos'][f"{week_text}({date_text})"] = venue_times
                                index += 1
                                print_with_timestamp(f"{place_name} Success================================")
                            output_data[place_name] = place_data
                        elif "验证" in str(watcher.driver.page_source):
                            print(f"[2] Processing by solving slider captcha...")
                            print_with_timestamp(f"{place_name} 需要验证，跳过处理。")
                            continue
                        else:
                            print("[3] 未知状态，跳过处理。")
                    except Exception as error:
                        print_with_timestamp(f"{place_name} failed: {str(error).splitlines()[0]}")
                upload_file_to_github(output_data)
                # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # print(output_data)
                # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            except Exception as e:
                print_with_timestamp(f"任务执行出错: {str(e)}")
            finally:
                # 确保资源被正确释放
                if watcher:
                    try:
                        watcher.teardown_driver()
                    except:
                        pass

            # 计算耗时
            cost_time = time.time() - start_time
            print_with_timestamp(f"本次任务耗时：{cost_time:.2f} 秒")
            
            # 计算需要休息的时间
            # 如果任务执行时间少于5分钟，则休息剩余时间；否则直接开始下一次循环
            sleep_time = max(0, 300 - cost_time)  # 300秒 = 5分钟
            if sleep_time > 0:
                print_with_timestamp(f"等待 {sleep_time:.2f} 秒后开始下一次任务...")
                time.sleep(sleep_time)
                
        except Exception as e:
            print_with_timestamp(f"发生意外错误: {str(e)}")
            print_with_timestamp("等待5分钟后重试...")
            time.sleep(300)
            continue
