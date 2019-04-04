import os
from flask import Flask, request, redirect, url_for,jsonify,make_response,send_file
from werkzeug.utils import secure_filename
from aip import AipSpeech
import pydub
import time
import datetime
import wave
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['wav', 'pcm','mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/asr/api/v1.0', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = str(int(time.time()))+ str(secure_filename(file.filename))[-6:]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pydub.AudioSegment.converter = 'E:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe'
            mp3_path = './uploads/' + str(filename)
            wav_path = './uploads/' + str(int(time.time())) + '.wav'
            wav_path = mp3_to_wav(mp3_path, wav_path)
            data = asr_data(wav_path)
            if data =='错误啦':
                tts_bd(data)
            else:
                data_tts='成功了,'+data
                tts_bd(data_tts)
            os.remove(mp3_path)
            os.remove(wav_path)
            return jsonify({'code':200,'data':data})
#生成语音
def tts_bd(text):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text, 'zh', 1, {'vol': 5})
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        filename = './download/tts.mp3'
        with open(filename, 'wb') as f:
            f.write(result)
        return filename
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def asr_data(filehello):
    # 识别本地文件
    result = client.asr(get_file_content(filehello), 'wav', 16000, {'dev_pid': 1536,})
    try:
        re_data = result['result'][0]
    except:
        re_data='错误啦'
    return re_data

@app.route('/asr/api/v1.0/tts', methods=['GET'])
def reportexport():
    basedirs = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'download')
    filenames = []
    for path, subdir, filename in os.walk(basedirs):
        for item in filename:
            filenames.append(os.path.join(path, item))
    if os.path.isfile(filenames[0]):
        response = make_response(send_file(filenames[0]))
        response.headers["Content-Disposition"] = "attachment; filename='%s'" % (u'tts.mp3')
        return response

def mp3_to_wav(mp3_path, wav_path):
    pydub.AudioSegment.converter = 'E:/ffmpeg/ffmpeg/bin/ffmpeg.exe'
    sound = pydub.AudioSegment.from_mp3(mp3_path)
    raw_data = sound._data
    size = len(raw_data)
    f = wave.open(wav_path, 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    f.setnframes(size)
    f.writeframes(raw_data)
    f.close()
    return wav_path
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6000)