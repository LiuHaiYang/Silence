# -*- coding: utf-8 -*-
# 需要安装pydub、ffmpeg
import pydub
import io
import wave
import subprocess
def mp3_to_wav(mp3_path, wav_path):
    # with open(mp3_path, 'rb') as fh:
    #     data = fh.read()
    #
    # aud = io.BytesIO(data)
    pydub.AudioSegment.converter = 'E:/ffmpeg/ffmpeg/bin/ffmpeg.exe'
    # sound = pydub.AudioSegment.from_file(aud, format='mp3')
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

mp3_to_wav('./uploads/auido.mp3', 'out.wav')