#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/28 17:45
@Author  : claudexie
@File    : app.py.py
@Software: PyCharm
"""
from flask import Flask, jsonify, request
import json
import datetime

app = Flask(__name__)

# 定义数据文件路径
DATA_FILE = '/home/lighthouse/data.json'


@app.route('/data', methods=['GET'])
def get_data():
    # 获取可选参数
    place_name = request.args.get('place_name')
    start_time = request.args.get('start_time')

    # 每次请求时重新加载数据文件
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)

        # 过滤数据
        filtered_data = data['data']

        if place_name:
            filtered_data = [entry for entry in filtered_data if entry.get('place_name') == place_name]

        if start_time:
            try:
                start_time_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                filtered_data = [entry for entry in filtered_data if datetime.datetime.strptime(
                    entry.get('start_time'), "%Y-%m-%d %H:%M:%S") >= start_time_dt]
            except ValueError:
                return jsonify({"error": "Invalid start_time format. Use YYYY-MM-DD HH:MM:SS"}), 400

        return jsonify({"data": filtered_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
