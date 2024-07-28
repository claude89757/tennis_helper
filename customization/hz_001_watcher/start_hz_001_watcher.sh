#!/bin/sh

# 检查是否传递了参数
if [ "$#" -ne 1 ]; then
    echo "用法: $0 <phone>"
    exit 1
fi
# 获取传递的参数
PHONE=$1

# 生成一个 1 到 200 之间的随机数
DELAY=$((RANDOM % 120 + 1))

# 输出当前时间和延迟时间
CURRENT_TIME_BEFORE=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$CURRENT_TIME_BEFORE] 将在 $DELAY 秒后启动 Python 程序..."

# 等待随机的延迟时间
sleep $DELAY

# 输出等待后的时间
CURRENT_TIME_AFTER=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$CURRENT_TIME_AFTER] Python 程序已启动。"

# 启动 Python 程序
/usr/bin/python3 /home/lighthouse/tennis_helper/customization/hz_001_watcher/hz_001_watcher.py --phone "$PHONE"  >> /home/lighthouse/tennis_helper/logs/hz_001_watcher_$(date +\%Y-\%m-\%d).log 2>&1
