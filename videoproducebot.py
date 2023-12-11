from flask import Flask, request, jsonify,render_template, abort,send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess
import threading
import time

# import main

# def install_and_run_script():
#     subprocess.Popen(['pip', 'install', '-r', 'requirements.txt'], shell=False).wait()
   



def run_script(filename):
    subprocess.Popen(['python', 'main.py', filename], shell=False)



app = Flask(__name__,template_folder='templates', static_folder='static')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    filename_save = secure_filename(file.filename)  
    
    file.save(filename_save)
    
    
    
    # install_and_run_script()

    # 創建一個新的線程來執行背景任務
    thread = threading.Thread(target=run_script, args=(filename_save,))
    thread.start()

    
    return render_template('index.html')
    



@app.route('/download/<filename>', methods=['GET'])

def download_file(filename):
    directory = os.getcwd()
    new_directory = directory + '/shorts'
    try:
        return send_from_directory(directory=new_directory , path=filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify(error='影片還在製作,請稍等'), 404


if __name__ == '__main__':
    app.run(debug=True)