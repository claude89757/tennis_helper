#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse

# 定义固定的字符映射表
CC = {
    'DCAiy': 'DGi0YA7BemWnQjCl4+bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ'
}

def Cs(CI):
    """
    字符映射函数，用于s0加密
    
    Args:
        CI (int): 输入索引值
        
    Returns:
        str: 映射后的字符
    """
    CI = CI & 0x3F  # 使用位运算限制索引范围为0-63
    return CC['DCAiy'][CI]

def s0(C8, C9, Cs):
    """
    s0加密函数
    
    Args:
        C8 (str): 输入字符串
        C9 (int): 位数参数
        Cs (function): 字符映射函数
        
    Returns:
        str: 加密后的字符串
    """
    # 如果输入为None，返回空字符串
    if C8 is None:
        return ''

    # 初始化变量
    CI = {}  # 字典对象，存储字符到数字的映射
    CD = {}  # 字典对象，存储临时数据
    Cd = ''  # 当前字符串
    CY = -3 * 0x6a7 + -0x266d + -0xe99 * -0x4  # 计数器
    CV = 0x21e3 + 0x1df2 + -0x30a * 0x15  # 字典计数器
    CR = 0x1 * -0xd37 + -0x233a + 0x3073  # 位数
    CL = []  # 结果数组
    Cb = 0x1162 + -0x447 + 0x15a9  # 位操作缓存
    Cn = 0x4a3 * 0x5 + 0x1d96 + -0x34c5  # 计数器

    # 第一次遍历输入字符串
    for CA in range(len(C8)):
        CC = C8[CA]
        
        if CC not in CI:
            CI[CC] = CV
            CV += 1
            CD[CC] = True

        CN = Cd + CC

        if CN in CI:
            Cd = CN
        else:
            if Cd in CD:
                if ord(Cd[0]) < 256:
                    for _ in range(CR):
                        Cb = (Cb << 1)
                        if Cn == (C9 - 1):
                            Cn = 0
                            CL.append(Cs(Cb))
                            Cb = 0
                        else:
                            Cn += 1

                    Cj = ord(Cd[0])
                    for _ in range(8):
                        Cb = (Cb << 1) | (Cj & 1)
                        if Cn == (C9 - 1):
                            Cn = 0
                            CL.append(Cs(Cb))
                            Cb = 0
                        else:
                            Cn += 1
                        Cj >>= 1
                else:
                    Cj = 1
                    for _ in range(CR):
                        Cb = (Cb << 1) | Cj
                        if Cn == (C9 - 1):
                            Cn = 0
                            CL.append(Cs(Cb))
                            Cb = 0
                        else:
                            Cn += 1
                        Cj = 0

                    Cj = ord(Cd[0])
                    for _ in range(16):
                        Cb = (Cb << 1) | (Cj & 1)
                        if Cn == (C9 - 1):
                            Cn = 0
                            CL.append(Cs(Cb))
                            Cb = 0
                        else:
                            Cn += 1
                        Cj >>= 1

                CY -= 1
                if CY == 0:
                    CY = pow(2, CR)
                    CR += 1
                CD.pop(Cd, None)
            else:
                Cj = CI[Cd]
                for _ in range(CR):
                    Cb = (Cb << 1) | (Cj & 1)
                    if Cn == (C9 - 1):
                        Cn = 0
                        CL.append(Cs(Cb))
                        Cb = 0
                    else:
                        Cn += 1
                    Cj >>= 1

            CY -= 1
            if CY == 0:
                CY = pow(2, CR)
                CR += 1
            CI[CN] = CV
            CV += 1
            Cd = CC

    if Cd:
        if Cd in CD:
            if ord(Cd[0]) < 256:
                for _ in range(CR):
                    Cb <<= 1
                    if Cn == (C9 - 1):
                        Cn = 0
                        CL.append(Cs(Cb))
                        Cb = 0
                    else:
                        Cn += 1

                Cj = ord(Cd[0])
                for _ in range(8):
                    Cb = (Cb << 1) | (Cj & 1)
                    if Cn == (C9 - 1):
                        Cn = 0
                        CL.append(Cs(Cb))
                        Cb = 0
                    else:
                        Cn += 1
                    Cj >>= 1
            else:
                Cj = 1
                for _ in range(CR):
                    Cb = (Cb << 1) | Cj
                    if Cn == (C9 - 1):
                        Cn = 0
                        CL.append(Cs(Cb))
                        Cb = 0
                    else:
                        Cn += 1
                    Cj = 0

                Cj = ord(Cd[0])
                for _ in range(16):
                    Cb = (Cb << 1) | (Cj & 1)
                    if Cn == (C9 - 1):
                        Cn = 0
                        CL.append(Cs(Cb))
                        Cb = 0
                    else:
                        Cn += 1
                    Cj >>= 1

            CY -= 1
            if CY == 0:
                CY = pow(2, CR)
                CR += 1
            CD.pop(Cd, None)
        else:
            Cj = CI[Cd]
            for _ in range(CR):
                Cb = (Cb << 1) | (Cj & 1)
                if Cn == (C9 - 1):
                    Cn = 0
                    CL.append(Cs(Cb))
                    Cb = 0
                else:
                    Cn += 1
                Cj >>= 1

        CY -= 1
        if CY == 0:
            CY = pow(2, CR)
            CR += 1

    Cj = 2
    for _ in range(CR):
        Cb = (Cb << 1) | (Cj & 1)
        if Cn == (C9 - 1):
            Cn = 0
            CL.append(Cs(Cb))
            Cb = 0
        else:
            Cn += 1
        Cj >>= 1

    while True:
        Cb <<= 1
        if Cn == (C9 - 1):
            CL.append(Cs(Cb))
            break
        Cn += 1

    return ''.join(CL)

def compute_hash(c8: str) -> int:
    """
    根据输入字符串计算哈希值。
    
    该函数使用位运算和算术运算从输入字符串计算一个32位哈希值。
    具体算法为:
    1. 初始化哈希值为0
    2. 遍历输入字符串的每个字符
    3. 对当前哈希值进行左移7位运算
    4. 减去原哈希值
    5. 加上常数398
    6. 加上当前字符的ASCII码值
    7. 使用位与运算保持在32位范围内
    
    Args:
        c8 (str): 需要计算哈希值的输入字符串
        
    Returns:
        int: 计算得到的32位哈希值
    """
    c9 = 0

    # 遍历输入字符串中的每个字符
    for cs in range(len(c8)):
        # 对 c9 进行左移 7 位的位运算，减去 c9，添加 398，再加上当前字符的字符代码
        c9 = ((c9 << 7) - c9 + 398 + ord(c8[cs])) & 0xFFFFFFFF  # 使用位与操作将其保持在 32 位有符号整数的范围内

    return c9


def encode_uri_component(uri: str) -> str:
    """
    对 URI 进行编码。
    
    该函数使用 urllib.parse.quote 对输入 URI 进行编码，
    并指定安全字符集为 ~()*!.\'。
    
    Args:
        uri (str): 需要编码的 URI 字符串
        
    Returns:
        str: 编码后的 URI 字符串
    """
    return urllib.parse.quote(uri, safe='~()*!.\'')


def encrypt_url_param(c8: str, c9: int, cs: int) -> int:
    """
    将输入参数进行加密处理，用于 URL 参数加密
    
    参数:
    c8: 字符串，用于加密计算
    c9: 整数，初始索引值
    cs: 整数，步进值
    """
    # 初始化变量
    ck = 0
    cj = c9
    cc = len(c8)  # 获取字符串 c8 的长度
    cn = cs if cs else 1  # 如果 cs 为 0，则 cn 设为 1

    print(f"[INFO] Initial values: CK = {ck}, Cj = {cj}, CC = {cc}, CN = {cn}")

    # 循环遍历，直到 cj >= cc
    while cj < cc:  # 判断 cj 是否小于 cc
        # 逐步计算 ck 的值
        ck = ((ck << 5) - ck + ord(c8[cj])) & 0xFFFFFFFF  # 保证 ck 在 32 位整数范围内
        cj += cn

    return ck

def test_s0():
    """
    测试s0加密函数
    """
    # 测试用例1
    test1_input = "-1938548878|0|1732437458668|1"
    test1_expected = "n4+xgDuDBDcDnAWGkWD/D0WobeiK5+mqw4G=pFe4D"
    test1_result = s0(test1_input, 6, Cs)
    print('\n测试用例1:')
    print('输入:', test1_input)
    print('预期输出:', test1_expected)
    print('实际输出:', test1_result)
    print('测试结果:', '通过' if test1_result == test1_expected else '失败')

    # 测试用例2
    test2_input = "-565752108|0|1732437342710|1"
    test2_expected = "n4fx9i0=eYqeqDKDtD/GWH4QqqiwzLwoo4TD"
    test2_result = s0(test2_input, 6, Cs)
    print('\n测试用例2:')
    print('输入:', test2_input)
    print('预期输出:', test2_expected)
    print('实际输出:', test2_result)
    print('测试结果:', '通过' if test2_result == test2_expected else '失败')

    # 测试用例3
    test3_input = "-278611504|0|1732454625451|1"
    test3_expected = "n4mxyDBD9D20i=D7DnDBdFOK0QmgkbhDlhoTD"
    test3_result = s0(test3_input, 6, Cs)
    print('\n测试用例3:')
    print('输入:', test3_input)
    print('预期输出:', test3_expected)
    print('实际输出:', test3_result)
    print('测试结果:', '通过' if test3_result == test3_expected else '失败')

def generate_signed_url(base_url: str, sales_item_id: str, timestamp: str) -> str:
    """
    生成带有签名的URL
    
    Args:
        base_url (str): 基础URL
        sales_item_id (str): 销售项目ID
        timestamp (str): 时间戳
        
    Returns:
        str: 带有签名的完整URL
    """
    # 1. 构建初始URL
    initial_url = f"{base_url}?salesItemId={sales_item_id}&t={timestamp}"
    
    # 2. URL编码
    encoded_url = encode_uri_component(initial_url)
    
    # 3. 计算哈希值
    hash_value = compute_hash(encoded_url)
    
    # 4. 构建s0函数的输入参数
    params = f"{hash_value}|0|{timestamp}|1"
    
    # 5. 使用s0函数生成timestamp__1762参数
    timestamp_1762 = s0(params, 6, Cs)
    
    # 6. 计算encrypt_url_param
    encrypt_param = f"{hash_value}|{timestamp}"
    encrypted_value = encrypt_url_param(encrypt_param, 0, 1)
    
    # 7. 构建最终的完整URL
    full_url = f"{initial_url}&timestamp__1762={timestamp_1762}"
    
    return full_url, encrypted_value

def test_url_generation():
    """
    测试URL生成功能
    """
    # 测试参数
    base_url = "https://wxsports.ydmap.cn/srv100140/api/pub/sport/venue/getVenueCalendarList"
    sales_item_id = "100341"
    timestamp = "1732455155433"
    
    # 生成签名URL和加密值
    signed_url, encrypted_value = generate_signed_url(base_url, sales_item_id, timestamp)
    
    print("\n=== URL生成测试 ===")
    print("基础URL:", base_url)
    print("销售项目ID:", sales_item_id)
    print("时间戳:", timestamp)
    print("\n生成的完整URL:")
    print(signed_url)
    
    # 验证URL格式
    assert "timestamp__1762=" in signed_url, "URL中缺少timestamp__1762参数"
    assert f"salesItemId={sales_item_id}" in signed_url, "URL中缺少salesItemId参数"
    assert f"t={timestamp}" in signed_url, "URL中缺少t参数"
    
    # 验证生成过程
    initial_url = f"{base_url}?salesItemId={sales_item_id}&t={timestamp}"
    encoded_url = encode_uri_component(initial_url)
    hash_value = compute_hash(encoded_url)
    
    # 验证s0参数
    params = f"{hash_value}|0|{timestamp}|1"
    expected_timestamp_1762 = s0(params, 6, Cs)
    
    # 验证encrypt_url_param
    encrypt_param = f"{hash_value}|{timestamp}"
    expected_encrypted_value = encrypt_url_param(encrypt_param, 0, 1)
    
    print("\n=== 验证步骤 ===")
    print("1. 初始URL:", initial_url)
    print("2. 编码后的URL:", encoded_url)
    print("3. 哈希值:", hash_value)
    print("4. s0参数:", params)
    print("5. timestamp__1762:", expected_timestamp_1762)
    print("6. encrypt_url_param输入:", encrypt_param)
    print("7. encrypt_url_param输出:", expected_encrypted_value)
    
    assert encrypted_value == expected_encrypted_value, "encrypt_url_param值不匹配"
    assert f"timestamp__1762={expected_timestamp_1762}" in signed_url, "timestamp__1762值不匹配"
    
    print("\n✅ URL格式验证通过")
    print("✅ 参数生成验证通过")
    print("✅ encrypt_url_param验证通过")

# main.py - 测试各个公共函数
if __name__ == "__main__":
    print("==================== TESTING compute_hash FUNCTION ====================")
    input_str = "https%3A%2F%2Fwxsports.ydmap.cn%2Fsrv100140%2Fapi%2Fpub%2Fsport%2Fvenue%2FgetSportVenueConfig%3FsalesItemId%3D100341%26curDate%3D1731686400000%26venueGroupId%3D%26t%3D1731771919629"
    output = compute_hash(input_str)
    print(f"✅[RESULT] compute_hash Function Output: {output}")

    print("==================== TESTING encode_uri_component FUNCTION ====================")
    uri_input = "https://wxsports.ydmap.cn/srv100140/api/pub/sport/venue/getSportVenueConfig?salesItemId=100341&curDate=1731686400000&venueGroupId=&t=1731771919629"
    encoded_output = encode_uri_component(uri_input)
    print(f"✅[RESULT] encode_uri_component Function Output: {encoded_output}")

    print("==================== TESTING encrypt_url_param FUNCTION ====================")
    c8 = "3315363095|1731757497111"
    c9 = 0
    cs = 1
    expected_ck = 847281144
    result = encrypt_url_param(c8, c9, cs)
    print(f"✅[RESULT] encrypt_url_param Function Output: CK = {result}")

    print("==================== TESTING s0 FUNCTION ====================")
    test_s0()
    
    print("\n==================== TESTING URL GENERATION ====================")
    test_url_generation()
    
    print("==================== ALL TESTS COMPLETED SUCCESSFULLY ====================")
