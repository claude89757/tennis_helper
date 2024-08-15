from quart import Quart, jsonify
import os
import aiofiles
app = Quart(__name__)

@app.route('/api/files', methods=['GET'])
async def get_files():
    directory = '/root'
    files_info = []

    for filename in os.listdir(directory):
        if filename.endswith('available_court.txt'):
            file_path = os.path.join(directory, filename)
            try:
                async with aiofiles.open(file_path, 'r') as file:
                    file_content = await file.read()
                files_info.append({
                    'filename': file_path,
                    'content': file_content
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    return jsonify(files_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
