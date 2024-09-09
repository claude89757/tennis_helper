from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


# 定义文件路径
file_path = 'ISZ_URL_MD5'


@app.route('/save_url_md5', methods=['POST'])
def save_md5():
    # 从请求中获取URL
    data = request.get_json()
    md5__1182 = data.get('md5__1182')

    if not md5__1182:
        logging.error("md5__1182 is required")
        return jsonify({"error": "md5__1182 is required"}), 400

    # 将MD5值写入文件
    with open(file_path, 'w') as file:
        file.write(md5__1182)

    logging.info(f"MD5 value {md5__1182} saved successfully")
    return jsonify({"message": "MD5 value saved successfully"}), 200


if __name__ == '__main__':
    app.run(port=5000)
