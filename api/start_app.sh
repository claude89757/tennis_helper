#!/bin/bash


# crontab
# */10 * * * * chmod +x /usr/bin/python3 /home/lighthouse/tennis_helper/api/start_app.sh && /usr/bin/python3 /home/lighthouse/tennis_helper/api/start_app.sh

# 定义日志文件路径
LOG_FILE="/home/lighthouse/tennis_helper/api/app.log"

# 检查app.py是否在运行
if pgrep -f "/usr/bin/python3 /home/lighthouse/tennis_helper/api/app.py" > /dev/null
then
    echo "$(date): app.py is running" >> $LOG_FILE
else
    echo "$(date): app.py is not running, starting it now" >> $LOG_FILE
    # 启动app.py
    nohup /usr/bin/python3 /home/lighthouse/tennis_helper/api/app.py >> $LOG_FILE 2>&1 &
    echo "$(date): app.py started" >> $LOG_FILE
fi
