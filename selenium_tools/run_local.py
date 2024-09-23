import time
import subprocess
import os
import sys
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

while True:
    env = os.environ.copy()
    env['GIT_TOKEN'] = ''

    try:
        logging.info("Starting get_data_by_chrome.py...")
        result = subprocess.run([sys.executable, '-u', 'get_data_by_chrome.py'], env=env, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess returned non-zero exit status {e.returncode}")
        logging.error(f"Command output: {e.output}")
        # 可以选择重新尝试或退出
        break
    except Exception as e:
        logging.exception("An unexpected error occurred:")
    else:
        logging.info("get_data_by_chrome.py executed successfully.")
    finally:
        logging.info("Waiting for 300 seconds before next run...")
        time.sleep(300)