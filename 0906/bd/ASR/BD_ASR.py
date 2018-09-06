# encoding:utf-8
from aip import AipSpeech
# APPID AK SK
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def asr_data(filehello):
    # 识别本地文件
    # result = client.asr(get_file_content('test2.pcm'), 'pcm', 16000, {'dev_pid': 1737,})
    # result = client.asr(get_file_content('../public/8k.pcm'), 'wav', 8000, {'dev_pid': 1536,})
    result = client.asr(get_file_content(filehello), 'wav', 16000, {'dev_pid': 1536,})
    print(result)
    re_data = result['result'][0]
    # BD_TTS.tts_bd(re_data)
    return re_data