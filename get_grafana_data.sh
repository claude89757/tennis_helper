#!/bin/bash

# 定义日志文件目录和目标JSON文件
LOG_DIR="/home/lighthouse/tennis_helper/logs"
TARGET_JSON="/home/lighthouse/data.json"

# 临时文件
TEMP_JSON="/tmp/temp_data.json"

# 清空临时文件
> $TEMP_JSON

# 查找以vip、hz和sh开头的.log文件中的特定日志数据，并记录每个文件找到的数据数量
for file in $LOG_DIR/{vip,hz,sh}*.log; do
    if [ -f "$file" ]; then
        echo "Searching in file: $file"
        count=$(awk '/\[GRAFANA_DATA\]@{/{match($0, /\[GRAFANA_DATA\]@{.*}/, arr); if (arr[0] != "") print substr(arr[0], 15)}' "$file" | tee -a $TEMP_JSON | wc -l)
        echo "File: $file, Found: $count entries"
    else
        echo "File not found: $file"
    fi
done

# 检查临时文件内容
echo "Temporary JSON data:"
cat $TEMP_JSON

# 如果临时文件不为空
if [ -s $TEMP_JSON ]; then
    # 读取现有的data.json文件
    if [ -f $TARGET_JSON ]; then
        EXISTING_DATA=$(cat $TARGET_JSON | jq -c '.data')
    else
        EXISTING_DATA="[]"
    fi

    # 读取新数据并验证其格式
    if jq -e . >/dev/null 2>&1 <<<$(cat $TEMP_JSON); then
        NEW_DATA=$(cat $TEMP_JSON | jq -c -s '.')
    else
        echo "Error: Invalid JSON data in $TEMP_JSON"
        exit 1
    fi

    # 合并新旧数据
    MERGED_DATA=$(echo $EXISTING_DATA $NEW_DATA | jq -s '.[0] + .[1]')

    # 写入到data.json文件
    echo "{\"data\": $MERGED_DATA}" > $TARGET_JSON
fi

# 清理临时文件
rm -f $TEMP_JSON