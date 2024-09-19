from flask import Flask, send_file, jsonify,send_from_directory
import subprocess
import os

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('../html/index.html')

@app.route('/favicon.ico')#设置icon
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../pic'),'huse.ico')#对于当前文件所在路径,比如这里是static下的favicon.ico
                               

@app.route('/run_command_and_get_image', methods=['POST'])
def run_command_and_get_image():
    try:
        # 运行指令
        subprocess.run(['python3', 'getQRCode.py'], check=True)

        # 获取图片
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pic/pay.png')
        return send_file(image_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_image')
def get_image():
    try:
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pic/pay.png')
        return send_file(image_path)
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
