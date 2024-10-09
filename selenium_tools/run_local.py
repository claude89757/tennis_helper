import time
import subprocess
import os
import sys
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while True:
    env = os.environ.copy()

    try:
        logging.info("Starting get_data_by_chrome.py...")
        result = subprocess.run([sys.executable, '-u', 'get_data_by_chrome_with_proxy.py'], env=env, check=True)
    except Exception as error:
        logging.exception(f"An unexpected error occurred: {error}")
        continue

    logging.info("get_data_by_chrome.py executed successfully.")
    logging.info("Waiting for 300 seconds before next run...")
    time.sleep(500)
