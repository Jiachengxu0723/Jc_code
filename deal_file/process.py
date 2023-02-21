import csv
import os
import numpy as np
from pydub import AudioSegment

path = './target_audio/train/'
audio_files = os.listdir(path)
audio_files = sorted(audio_files)
for audio_file in audio_files:
    audio_file = path + audio_file
    audio = AudioSegment.from_wav(audio_file)
    # 获取音频时长
    duration = audio.duration_seconds
    audio_file = os.path.splitext(audio_file)[0]
    txt_file = audio_file.replace('target_audio', 'txt') + '.txt'
    rows = []
    with open(txt_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows.append(row)
    label_duration = rows[-1][0].split('	')[1]
    if float(label_duration) - duration > 0.1:
        print(f'{audio_file}')

