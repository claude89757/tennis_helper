from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/api/files', methods=['GET'])
def get_files():
    directory = '/root'
    files_info = []

    # 遍历目录中的文件
    for filename in os.listdir(directory):
        if filename.endswith('available_court.txt'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                files_info.append({
                    'filename': file_path,
                    'content': file_content
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    return jsonify(files_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

