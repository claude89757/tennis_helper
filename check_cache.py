import shelve
import argparse

if __name__ == '__main__':
    # 创建命令行解析器, 添加命令行参数
    parser = argparse.ArgumentParser(description='Help Message')
    parser.add_argument('--court_name', type=str, help='Tennis Court Name')

    # 解析命令行参数
    args = parser.parse_args()
    print(args.court_name)

    with shelve.open(f'{args.court_name}_cache') as db:
        for key, value in db.items():
            print(f'{key}: {value}')
