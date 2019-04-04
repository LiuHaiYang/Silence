# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask,request,make_response,send_file,jsonify,redirect,url_for
from flask_restful import Api, Resource
import os
from aip import AipSpeech
app = Flask(__name__)
api = Api(app)


class ASRTest(Resource):
    def __init__(self):
        # APPID AK SK
        self.APP_ID = ''
        self.API_KEY = ''
        self.SECRET_KEY = ''
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.UPLOAD_FOLDER = './uploads'
        self.ALLOWED_EXTENSIONS = set(['wav', 'pcm','mp3'])

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    def post(self):
        file = request.files['file']
        print('++++++++')
        print(file.filename)
        if file and self.allowed_file(file.filename):
            filename = self.secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = self.asr_data(filename)
            print(data)

    # 读取文件
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def asr_data(self,filehello):
        # 识别本地文件
        result = self.client.asr(self.get_file_content(filehello), 'wav', 16000, {'dev_pid': 1536,})
        print(result)
        re_data = result['result'][0]
        # BD_TTS.tts_bd(re_data)
        print(re_data)
        return re_data

api.add_resource(ASRTest, '/ASRTest/api/v1')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)