#!/bin/bash

# 定义日志文件目录和目标JSON文件
LOG_DIR="/home/lighthouse/tennis_helper/logs"
TARGET_JSON="/home/lighthouse/data.json"

# 临时文件
TEMP_JSON="/tmp/temp_data.json"

# 查找以vip、hz和sh开头的.log文件中的特定日志数据
grep -h -o 'print(F"OUTPUT_DATA@\{.*\}")' $LOG_DIR/{vip,hz,sh}*.log | sed 's/print(F"OUTPUT_DATA@//' | sed 's/")//' > $TEMP_JSON

# 如果临时文件不为空
if [ -s $TEMP_JSON ]; then
    # 读取现有的data.json文件
    if [ -f $TARGET_JSON ]; then
        EXISTING_DATA=$(cat $TARGET_JSON | jq -c '.data')
    else
        EXISTING_DATA="[]"
    fi

    # 读取新数据
    NEW_DATA=$(cat $TEMP_JSON | jq -c -s '.')

    # 合并新旧数据
    MERGED_DATA=$(echo $EXISTING_DATA $NEW_DATA | jq -s '.[0] + .[1]')

    # 写入到data.json文件
    echo "{\"data\": $MERGED_DATA}" > $TARGET_JSON
fi

# 清理临时文件
rm -f $TEMP_JSON