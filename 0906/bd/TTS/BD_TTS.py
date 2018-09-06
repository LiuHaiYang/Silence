# encoding:utf-8
from aip import AipSpeech
import time
# APPID AK SK
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

def tts_bd(text):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text, 'zh', 1, {'vol': 5})
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        filename = str(time.time())+'.mp3'
        with open(filename, 'wb') as f:
            f.write(result)