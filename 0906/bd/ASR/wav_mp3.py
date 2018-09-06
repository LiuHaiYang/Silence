from pydub import AudioSegment
AudioSegment.converter = "e:\ffmpeg\ffmpeg\bin\ffmpeg.exe"

wav = AudioSegment.from_wav('./uploads/16k.wav')  #If I execute only this line, there are no errors.
wav.export(r"WavOut.mp3",format="mp3")