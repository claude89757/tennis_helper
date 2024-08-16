#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/16 15:03
@Author  : claude
@File    : redis_client.py
@Software: PyCharm
"""

import os
import redis
import json
import time
import uuid
from datetime import datetime


class RedisClient:
    def __init__(self, db=0):
        self.redis_conn = redis.Redis(
            host=os.environ['REDIS_HOST'],
            port=os.environ['REDIS_PORT'],
            password=os.environ['REDIS_PASSWORD'],
            db=db,
            decode_responses=True  # 自动解码为字符串
        )

    def _print_with_timestamp(self, message):
        """打印带时间戳的消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def _get_lock_name(self, key):
        """根据键名生成锁的名称"""
        return f"lock:{key}"

    def acquire_lock(self, lock_name, acquire_timeout=10, lock_timeout=10):
        """获取分布式锁"""
        identifier = str(uuid.uuid4())  # 唯一标识符
        end = time.time() + acquire_timeout
        while time.time() < end:
            if self.redis_conn.set(lock_name, identifier, ex=lock_timeout, nx=True):
                self._print_with_timestamp(f"Lock '{lock_name}' acquired with identifier '{identifier}'")
                return identifier
            time.sleep(0.01)  # 短暂休眠避免高频竞争
        self._print_with_timestamp(f"Failed to acquire lock '{lock_name}'")
        return None

    def release_lock(self, lock_name, identifier):
        """释放分布式锁"""
        pipeline = self.redis_conn.pipeline(True)
        while True:
            try:
                pipeline.watch(lock_name)
                if pipeline.get(lock_name) == identifier:
                    pipeline.multi()
                    pipeline.delete(lock_name)
                    pipeline.execute()
                    self._print_with_timestamp(f"Lock '{lock_name}' released")
                    return True
                pipeline.unwatch()
                break
            except redis.WatchError:
                pass
        self._print_with_timestamp(f"Failed to release lock '{lock_name}'")
        return False

    def get_json_data(self, key, use_lock=False, lock_timeout=10):
        """读取Redis的数据，加载成JSON格式"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return None

        try:
            data = self.redis_conn.get(key)
            if data:
                if isinstance(data, bytes):  # 如果数据是字节类型，需要解码为字符串
                    data = data.decode('utf-8')
                json_data = json.loads(data)
                self._print_with_timestamp(f"Retrieved JSON data for key '{key}' with length {len(json_data)}")
                return json_data
            self._print_with_timestamp(f"No data found for key '{key}'")
            return None
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def set_json_data(self, key, value, timeout=600, use_lock=False, lock_timeout=10):
        """写入Redis的数据，JSON格式，并能设置超时时间，默认600秒超时"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            json_data = json.dumps(value)
            self.redis_conn.set(key, json_data, ex=timeout)
            self._print_with_timestamp(f"Set JSON data for key '{key}' with length {len(value)} and timeout {timeout} seconds")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def get_str_data(self, key, use_lock=False, lock_timeout=10):
        """读取Redis的数据，字符串格式"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return None

        try:
            data = self.redis_conn.get(key)
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if data:
                self._print_with_timestamp(f"Retrieved string data for key '{key}' with length {len(data)}")
            else:
                self._print_with_timestamp(f"No data found for key '{key}'")
            return data
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def set_str_data(self, key, value, timeout=600, use_lock=False, lock_timeout=10):
        """写入Redis的数据，字符串格式，并能设置超时时间，默认600秒超时"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            self.redis_conn.set(key, value, ex=timeout)
            self._print_with_timestamp(f"Set string data for key '{key}' with length {len(value)} and timeout {timeout} seconds")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def reset_timeout(self, key, timeout=600, use_lock=False, lock_timeout=10):
        """重置指定key的超时时间"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            if self.redis_conn.exists(key):
                self.redis_conn.expire(key, timeout)
                self._print_with_timestamp(f"Reset timeout for key '{key}' to {timeout} seconds")
            else:
                self._print_with_timestamp(f"Key '{key}' does not exist.")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def delete_data(self, key, use_lock=False, lock_timeout=10):
        """删除Redis中的指定key，如果键存在则删除"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            if self.redis_conn.exists(key):
                result = self.redis_conn.delete(key)
                if result:
                    self._print_with_timestamp(f"Key '{key}' deleted.")
                else:
                    self._print_with_timestamp(f"Failed to delete key '{key}'.")
            else:
                self._print_with_timestamp(f"Key '{key}' does not exist.")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def get_json_data_by_prefix(self, prefix, use_lock=False, lock_timeout=10):
        """查询所有以某个字符串开头的key，并返回这些key对应的JSON数据"""
        identifier = None
        lock_name = self._get_lock_name(prefix) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return {}

        try:
            keys = self.redis_conn.keys(f"{prefix}*")
            results = {}
            for key in keys:
                data = self.get_json_data(key)
                if data:
                    results[key] = data
            self._print_with_timestamp(f"Retrieved JSON data for keys with prefix '{prefix}' (Total keys: {len(keys)})")
            return results
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def update_json_data(self, key, updates, use_lock=False, lock_timeout=10):
        """更新Redis中的JSON数据，如果不存在则初始化一个空的字段"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            existing_data = self.get_json_data(key)
            if not existing_data:
                self._print_with_timestamp(
                    f"No existing JSON data found for key '{key}', initializing with an empty dictionary")
                existing_data = {}  # 初始化为空字典

            # 更新现有的数据
            existing_data.update(updates)
            self.set_json_data(key, existing_data, use_lock=False)
            self._print_with_timestamp(f"Updated JSON data for key '{key}' with updates: {updates}")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def get_int_data(self, key, use_lock=False, lock_timeout=10):
        """获取Redis中存储的整数数据"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return None

        try:
            data = self.redis_conn.get(key)
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if data is not None:
                int_data = int(data)
                self._print_with_timestamp(f"Retrieved integer data for key '{key}': {int_data}")
                return int_data
            self._print_with_timestamp(f"No data found for key '{key}'")
            return None
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def set_int_data(self, key, value, timeout=600, use_lock=False, lock_timeout=10):
        """设置Redis中的整数数据，并能设置超时时间，默认600秒超时"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            self.redis_conn.set(key, int(value), ex=timeout)
            self._print_with_timestamp(
                f"Set integer data for key '{key}' with value {value} and timeout {timeout} seconds")
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)

    def increment_int_data(self, key, amount=1, use_lock=False, lock_timeout=10):
        """原子性地递增或递减Redis中的整数数据"""
        identifier = None
        lock_name = self._get_lock_name(key) if use_lock else None
        if use_lock:
            identifier = self.acquire_lock(lock_name, lock_timeout=lock_timeout)
            if not identifier:
                return

        try:
            new_value = self.redis_conn.incrby(key, amount)
            self._print_with_timestamp(f"Incremented integer data for key '{key}' by {amount}. New value: {new_value}")
            return new_value
        finally:
            if identifier:
                self.release_lock(lock_name, identifier)


# 示例使用
if __name__ == "__main__":
    # 初始化RedisClient实例
    redis_client = RedisClient(
        db=0
    )

    # 示例：使用锁写入JSON数据
    redis_client.set_json_data('user:1001', {'name': 'Alice', 'age': 30}, use_lock=True)

    # 示例：使用锁读取JSON数据
    data = redis_client.get_json_data('user:1001', use_lock=True)
    print(data)
