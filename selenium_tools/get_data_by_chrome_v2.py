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
import tempfile
import zipfile
import string

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

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
        response = requests.get(url)
        text = response.text.strip()
        lines = text.split("\n")
        lines = [line.strip() for line in lines]
        proxies.extend(lines)
        print(f"Loaded {len(lines)} proxies from {url}")
    print(f"Total {len(proxies)} proxies loaded")
    random.shuffle(proxies)
    return proxies


def upload_file_to_github(input_data):
    token = os.environ['GIT_TOKEN']
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
        print(F"File uploaded successfully, total {len(input_data)} data")
    else:
        print("Failed to upload file:", response.status_code, response.text)


def get_file_sha(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None


class TwitterWatcher:
    def __init__(self, timeout=10, headless: bool = True, driver_mode='local'):
        self.timeout = timeout
        self.interaction_timeout = 10
        self.driver = None
        self.headless = headless
        self.driver_mode = driver_mode  # 'local' or 'remote'

    def setup_driver(self, proxy=None, proxy_auth=None):
        """
        初始化浏览器
        """
        chrome_options = webdriver.ChromeOptions()
        if not self.headless:
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.headless = True
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--no-sandbox")

        # Disable automation flags to avoid detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # General options to mimic regular browser behavior
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-quic')
        chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--ignore-ssl-errors')

        # Random User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.5938.62 Safari/537.36",
        ]
        random_user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={random_user_agent}")

        # Proxy settings
        if proxy:
            if proxy_auth:
                pluginfile = self._create_proxy_auth_extension(
                    proxy_host=proxy['host'],
                    proxy_port=proxy['port'],
                    proxy_username=proxy_auth['username'],
                    proxy_password=proxy_auth['password']
                )
                chrome_options.add_extension(pluginfile)
            else:
                chrome_options.add_argument(f'--proxy-server={proxy}')
        else:
            pass

        # Initialize driver
        if self.driver_mode == 'local':
            service = Service("/usr/local/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        elif self.driver_mode == 'remote':
            selenium_grid_url = 'http://localhost:4444/wd/hub'
            self.driver = webdriver.Remote(command_executor=selenium_grid_url, options=chrome_options)
        else:
            raise ValueError(f"Invalid driver mode: {self.driver_mode}")

        self.random_delay(min_delay=2, max_delay=5)

        # Execute stealth JavaScript to mask automation properties
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = {
                runtime: {}
            };
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            """
        })

        # Remove cdc_ variables
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            for (let property in window) {
                if (property.match(/^cdc_/)) {
                    delete window[property];
                }
            }
            """
        })

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

        # Click and hold the slider
        action_chains.click_and_hold(slider).perform()
        time.sleep(random.uniform(0.5, 1.0))

        # Simulate human-like slider movement
        total_offset = 300
        current_offset = 0
        while current_offset < total_offset:
            move_by = random.randint(10, 30)
            action_chains.move_by_offset(move_by, 0).perform()
            current_offset += move_by
            time.sleep(random.uniform(0.01, 0.03))

        # Release the slider
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

    def _create_proxy_auth_extension(self, proxy_host, proxy_port, proxy_username, proxy_password,
                                     scheme='http'):
        """Creates a proxy authentication extension"""
        manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    }
}
        """

        background_js = string.Template("""
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "${scheme}",
            host: "${host}",
            port: parseInt(${port})
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({ value: config, scope: "regular" }, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "${username}",
            password: "${password}"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    { urls: ["<all_urls>"] },
    ["blocking"]
);
        """).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme
        )

        pluginfile = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return pluginfile.name


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


if __name__ == '__main__':
    """
    遍历查询多个网球场的信息，并缓存到 GitHub 上
    """

    parser = argparse.ArgumentParser(description='Script to fetch data.')
    parser.add_argument('--driver-mode', choices=['local', 'remote'], default='local',
                        help='Driver mode: local or remote (default: local)')
    args = parser.parse_args()
    driver_mode = args.driver_mode

    # Skip execution between midnight and 8 AM
    now = datetime.datetime.now().time()
    if datetime.time(0, 0) <= now < datetime.time(8, 0):
        print_with_timestamp('Skipping task execution between 0am and 8am')
        exit()
    else:
        print_with_timestamp('Executing task at {}'.format(datetime.datetime.now()))

    start_time = time.time()
    print("Setting up driver...")

    # Proxy settings
    proxy_auth = {
        'username': '5c9f99950c50d70a',
        'password': 'RNW78Fm5'
    }
    proxy = {
        'host': 'res.proxy-seller.com',
        'port': 10000
    }

    watcher = TwitterWatcher(headless=True, driver_mode=driver_mode)
    watcher.setup_driver(proxy=proxy, proxy_auth=proxy_auth)
    print("Driver setup complete.")

    # Start browsing
    url = "https://wxsports.ydmap.cn/booking/schedule/100220?salesItemId=100000"
    try:
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

        watcher.random_delay(min_delay=1, max_delay=10)

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
            "大沙河": "https://wxsports.ydmap.cn/booking/schedule/100220?salesItemId=100000",
            "黄木岗": "https://wxsports.ydmap.cn/booking/schedule/101333?salesItemId=100344",
            "华侨城": "https://wxsports.ydmap.cn/booking/schedule/105143?salesItemId=105347",
            "简上": "https://wxsports.ydmap.cn/booking/schedule/103909?salesItemId=102913",
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

                        if body_table:
                            tbody = body_table.find('tbody')
                            if tbody:
                                body_rows = tbody.find_all('tr')
                            else:
                                body_rows = body_table.find_all('tr')
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
                                    cell_class_name = cell.get("class")
                                    cell_class_name_list = str(cell_class_name).split()
                                    if len(cell_class_name_list) == 1:
                                        real_status = "可预订"
                                    else:
                                        real_status = "已预订"

                                    if col_index < num_cols:
                                        venue = venue_names[col_index]
                                        div_in_cell = cell.find('div')
                                        if div_in_cell:
                                            full_text = div_in_cell.get_text(separator=',', strip=False)
                                            time_matches = time_pattern.findall(full_text)
                                            time_slot = '-'.join(time_matches) if time_matches else ''
                                            temp_text = time_pattern.sub('', full_text)
                                            status = temp_text.strip()
                                            venue_times[venue].append({
                                                'time': time_slot,
                                                'status': real_status,
                                                'raw_status': status,
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
                    print("[3] 未知状态，跳过处理。")
            except Exception as error:
                print_with_timestamp(f"{place_name} failed: {str(error).splitlines()[0]}")
        upload_file_to_github(output_data)
    finally:
        watcher.teardown_driver()

    cost_time = time.time() - start_time
    print_with_timestamp(f"Total cost time：{cost_time} s")
