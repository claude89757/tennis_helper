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

# 读取本地JSON文件
with open('/home/lighthouse/data.json', 'r') as file:
    data = json.load(file)


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

