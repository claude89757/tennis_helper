from quart import Quart, jsonify
import os
import aiofiles
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Quart(__name__)

@app.route('/api/files', methods=['GET'])
async def get_files():
    directory = '/root'
    files_info = []

    logger.debug(f'Listing files in directory: {directory}')

    for filename in os.listdir(directory):
        if filename.endswith('available_court.txt'):
            file_path = os.path.join(directory, filename)
            logger.debug(f'Processing file: {file_path}')
            try:
                async with aiofiles.open(file_path, 'r') as file:
                    file_content = await file.read()
                files_info.append({
                    'filename': file_path,
                    'content': file_content
                })
                logger.info(f'File read successfully: {file_path}')
            except Exception as e:
                logger.error(f'Error reading file {file_path}: {str(e)}')
                return jsonify({'error': str(e)}), 500

    logger.info(f'Returning {len(files_info)} files')
    return jsonify(files_info)

if __name__ == '__main__':
    logger.info('Starting Quart application')
    app.run(host='0.0.0.0', port=5000)
