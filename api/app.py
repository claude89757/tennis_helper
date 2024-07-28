#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/28 17:45
@Author  : claudexie
@File    : app.py.py
@Software: PyCharm
"""
from flask import Flask, jsonify
import json

app = Flask(__name__)

# 定义数据文件路径
DATA_FILE = '/home/lighthouse/data.json'


@app.route('/data', methods=['GET'])
def get_data():
    # 每次请求时重新加载数据文件
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
