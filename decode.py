def decode_hex_string(hex_str):
    # 移除引号
    hex_str = hex_str.strip("'").strip('"')
    # 分割成单个 \x 序列
    parts = hex_str.split('\\x')[1:]
    # 转换每个十六进制值为字符
    chars = [chr(int(p, 16)) for p in parts]
    return ''.join(chars)

# 测试样例
test_strings = [
    '\\x63\\x73\\x4f\\x4b\\x51',
    '\\x6f\\x47\\x44\\x4c\\x58\\x67',
    '\\x73\\x41\\x50\\x57\\x7a\\x78',
    '\\x4b\\x67\\x50\\x46\\x55\\x4b',
    '\\x46\\x63\\x45\\x43\\x74\\x47',
    '\\x46\\x48\\x66\\x6e\\x6f\\x56'
]

for s in test_strings:
    print(f"{s} => {decode_hex_string(s)}") 