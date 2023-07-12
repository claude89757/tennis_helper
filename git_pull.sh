#!/bin/bash

# 定义目录路径
dir_path="/home/lighthouse/tennis_helper"

# 定义日志文件路径
log_file="$1"

# 进入目录
cd $dir_path

# 执行git pull并将输出重定向到日志文件，每次执行都覆盖之前的日志
git pull > $log_file 2>&1