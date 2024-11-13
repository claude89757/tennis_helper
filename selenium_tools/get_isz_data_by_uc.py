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
import concurrent.futures
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc

FILENAME = "isz_data_infos.json"
COOKIES_FILE = 'cookies.json'
HEADERS_FILE = 'headers.json'
PROXIES_CACHE_FILE = 'proxies_cache.txt'


def generate_proxies():
    """
    获取代理列表，优先使用本地缓存，如果本地缓存无效则从GitHub获取
    """
    # 首先尝试使用本地缓存
    if os.path.exists(PROXIES_CACHE_FILE):
        print("发现本地代理缓存文件")
        with open(PROXIES_CACHE_FILE, 'r') as f:
            cached_proxies = [line.strip() for line in f.readlines()]
        if cached_proxies:
            print(f"从本地缓存加载了 {len(cached_proxies)} 个代理")
            random.shuffle(cached_proxies)
            return cached_proxies

    # 如果本地缓存不存在或为空，从GitHub获取
    print("从GitHub获取代理列表")
    urls = [
        "https://raw.githubusercontent.com/claude89757/free_https_proxies/main/isz_https_proxies.txt"
    ]
    proxies = []

    for url in urls:
        print(f"getting proxy list for {url}")
        try:
            response = requests.get(url, timeout=30)
            text = response.text.strip()
            lines = text.split("\n")
            lines = [line.strip() for line in lines]
            proxies.extend(lines)
            print(f"Loaded {len(lines)} proxies from {url}")
        except Exception as e:
            print(f"从GitHub获取代理失败: {str(e)}")
            return []

    # 保存到本地缓存
    if proxies:
        try:
            with open(PROXIES_CACHE_FILE, 'w') as f:
                f.write('\n'.join(proxies))
            print(f"已将 {len(proxies)} 个代理保存到本地缓存")
        except Exception as e:
            print(f"保存代理到本地缓存失败: {str(e)}")

    print(f"Total {len(proxies)} proxies loaded")
    random.shuffle(proxies)
    return proxies


def upload_file_to_github(input_data):
    token = os.environ.get('GIT_TOKEN')
    repo = 'claude89757/tennis_data'
    url = f'https://api.github.com/repos/{repo}/contents/{FILENAME}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    content = json.dumps(input_data, ensure_ascii=False, indent=4)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    data = {
        'message': f'Update data',
        'content': encoded_content,
        'sha': get_file_sha(url, headers)
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"File uploaded successfully, total {len(input_data)} data")
    else:
        print("url: ", url)
        print("headers: ", headers)
        # print("data: ", data)
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
        自动适配当前Chrome版本和显示器大小
        """
        print("开始初始化Chrome驱动...")

        # 初始化Chrome选项
        chrome_options = uc.ChromeOptions()
        print("Chrome选项初始化完成")

        # 基础设置 - 自动适配显示器
        if not self.headless:
            # 不设置固定大小，让浏览器自动适配显示器
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-gpu")
            print("设置为可视化模式，将自动适配显示器大小")
        else:
            # 无头模式仍然需要固定大小
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
    如果本地缓存中的代理都不可用，则删除缓存文件并重新获取
    """
    proxies = generate_proxies()
    if not proxies:
        print("未获取到任何代理")
        return None

    print(f"开始测试 {len(proxies)} 个代理...")

    # 使用线程池并发测试代理
    working_proxy_found = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result:
                    working_proxy_found = True
                    return result
            except Exception as e:
                print(f"测试代理时发生错误 {proxy}: {str(e)}")

    # 如果没有找到可用代理，且使用的是缓存文件，则删除缓存文件并重试
    if not working_proxy_found and os.path.exists(PROXIES_CACHE_FILE):
        print("本地缓存中没有可用代理，删除缓存文件")
        try:
            os.remove(PROXIES_CACHE_FILE)
            print("缓存文件已删除，尝试重新获取代理")
            # 递归调用自身，重新获取代理
            return get_working_proxy()
        except Exception as e:
            print(f"删除缓存文件失败: {str(e)}")

    return None


if __name__ == '__main__':
    """
    遍历查询多个网球场的信息，并缓存到 GitHub 上
    每5分钟执行一次，失败直接开始下一轮
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
                    print("未找到可用代理，直接开始下一轮")
                    continue
            except Exception as e:
                print(f"获取代理时出错: {str(e)}，直接开始下一轮")
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

                            # 开始优化的部分，使用 Selenium 直接获取数据
                            date_slider = WebDriverWait(watcher.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'slider-box-datetime'))
                            )

                            date_elements = date_slider.find_elements(By.CLASS_NAME, 'new-datetime')

                            for index in range(len(date_elements)):
                                # 重新获取日期元素，防止 StaleElementReferenceException
                                date_slider = WebDriverWait(watcher.driver, 10).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'slider-box-datetime'))
                                )
                                date_elements = date_slider.find_elements(By.CLASS_NAME, 'new-datetime')
                                date_element = date_elements[index]

                                date_text = date_element.find_element(By.CLASS_NAME, 'datetime').text
                                week_text = date_element.find_element(By.CLASS_NAME, 'week').text

                                date_element.click()
                                watcher.random_delay(min_delay=2, max_delay=6)

                                print(f"Processing date: {date_text} {week_text}")

                                # 等待表格加载
                                WebDriverWait(watcher.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '.schedule-table tbody'))
                                )

                                # 获取场地名称
                                header_cells = watcher.driver.find_elements(By.CSS_SELECTOR, '.schedule-table thead th')
                                venue_names = [cell.text.strip() for cell in header_cells if cell.text.strip()]
                                print(f"Venue names: {venue_names}")

                                venue_times = {venue: [] for venue in venue_names}

                                # 获取表格行
                                body_rows = watcher.driver.find_elements(By.CSS_SELECTOR, '.schedule-table tbody tr')
                                print(f"Number of rows: {len(body_rows)}")

                                num_cols = len(venue_names)
                                occupied_cells = set()

                                time_pattern = re.compile(r'\d{2}:\d{2}-\d{2}:\d{2}')

                                def expand_cell(row_index, col_index, rowspan, colspan):
                                    for i in range(row_index, row_index + rowspan):
                                        for j in range(col_index, col_index + colspan):
                                            occupied_cells.add((i, j))

                                for row_index, row in enumerate(body_rows):
                                    # print(f"Processing row {row_index}")
                                    col_index = 0
                                    cells = row.find_elements(By.CSS_SELECTOR, 'td, th')
                                    # print(f"Number of cells in row {row_index}: {len(cells)}")
                                    cell_index = 0

                                    while col_index < num_cols and cell_index < len(cells):
                                        cell = cells[cell_index]
                                        while (row_index, col_index) in occupied_cells:
                                            col_index += 1

                                        rowspan = int(cell.get_attribute('rowspan') or '1')
                                        colspan = int(cell.get_attribute('colspan') or '1')
                                        # print(f"Cell at row {row_index}, col {col_index}: rowspan={rowspan}, colspan={colspan}")

                                        if col_index < num_cols:
                                            venue = venue_names[col_index]
                                            try:
                                                div_in_cell = cell.find_element(By.TAG_NAME, 'div')
                                            except NoSuchElementException:
                                                # print(f"No <div> found in cell at row {row_index}, col {col_index}")
                                                # 如果没有 <div>，可以选择跳过或处理其他逻辑
                                                expand_cell(row_index, col_index, rowspan, colspan)
                                                col_index += colspan
                                                cell_index += 1
                                                continue

                                            full_text = div_in_cell.text
                                            # print(f"Cell text at row {row_index}, col {col_index}: {full_text}")
                                            time_matches = time_pattern.findall(full_text)
                                            time_slot = '-'.join(time_matches) if time_matches else ''
                                            # print(f"Time slot: {time_slot}")

                                            # 获取状态信息
                                            spans = div_in_cell.find_elements(By.TAG_NAME, 'span')
                                            
                                            # 获取第一个 span 的文本
                                            show_status = spans[0].text.strip()
                                            if "元" in show_status:
                                                real_status = "可预订"
                                            else:
                                                real_status = show_status
                                            
                                            # # 测试
                                            # show_status_list = []
                                            # for span in spans:
                                            #     show_status = span.text.strip()
                                            #     show_status_list.append(show_status)
                                            # print(f"Show status list: {show_status_list}")
                                            # show_status = show_status_list[0]

                                            # print(f"Show status: {show_status}, Real status: {real_status}")
                                            
                                            venue_times[venue].append({
                                                'time': time_slot,
                                                'status': real_status,
                                                'show_status': show_status.strip(),
                                            })

                                        expand_cell(row_index, col_index, rowspan, colspan)
                                        col_index += colspan
                                        cell_index += 1

                                place_data['court_infos'][f"{week_text}({date_text})"] = venue_times
                                print_with_timestamp(f"{place_name} Success================================")
                                print(venue_times)
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
                print_with_timestamp(f"任务执行出错: {str(e)}，直接开始下一轮")
                continue
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
            print_with_timestamp(f"发生意外错误: {str(e)}，直接开始下一轮")
            continue
