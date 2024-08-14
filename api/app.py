#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/28 17:45
@Author  : claudexie
@File    : app.py
@Software: PyCharm
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/available_courts', methods=['GET'])
def get_available_courts():
    """
    查询 /root 文件夹下的 available_court.txt 结尾的文件，并返回其内容
    """
    local_path = "/root"
    matching_files = []

    try:
        for root, dirs, files in os.walk(local_path):
            for file in files:
                if file.endswith('available_court.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    matching_files.append({
                        'filename': file_path,
                        'content': file_content
                    })

        return jsonify({"data": matching_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
