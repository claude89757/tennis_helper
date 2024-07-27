#!/bin/sh

# 检查是否传递了参数
if [ "$#" -ne 1 ]; then
    echo "用法: $0 <phone>"
    exit 1
fi

# 获取传递的参数
PHONE=$1

# 生成一个 1 到 200 之间的随机数
DELAY=$((RANDOM % 200 + 1))

# 输出延迟时间
echo "将在 $DELAY 秒后启动 Python 程序..." >> /home/lighthouse/tennis_helper/logs/sh_002_watcher_$(date +\%Y-\%m-\%d).log 2>&1

# 等待随机的延迟时间
sleep $DELAY

# 启动 Python 程序
/usr/bin/python3 /home/lighthouse/tennis_helper/customization/sh_002_watcher/sh_002_watcher.py --phone "$PHONE"  >> /home/lighthouse/tennis_helper/logs/sh_002_watcher_$(date +\%Y-\%m-\%d).log 2>&1