# 参考 ：https://www.twblogs.net/a/5bed81022b717720b51fa34f
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import os


def get_file_list(directory, types = ['.wav'], is_sort = True):
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list


def cut_audio(audio_file, step=1000):
    audio = AudioSegment.from_wav(audio_file)
    length = len(audio)
    cut_parameters = np.arange(step, length, step)
    start_time = 0
    for stop_time in cut_parameters:
        audio_chunk = audio[start_time:stop_time]
        if not os.path.exists('./cut_data'):
            os.makedirs('./cut_data')
        label = os.path.basename(audio_file).split('.')[0]
        if 'cheer' in label:
            cut_data = f"./cut_data/{label}_{str(int(stop_time / 1000)).zfill(4)}.wav"
        else:
            cut_data = f"./cut_data/{label}_{str(int(stop_time / 1000)).zfill(4)}.wav"
        if not os.path.exists(cut_data):
            audio_chunk.export(cut_data, format="wav")
        start_time = stop_time


def get_total_duration():
    cut_files = get_file_list(cut_data_path,types='.wav')
    total_duration = 0
    for cut_file in cut_files:
        audio = AudioSegment.from_wav(cut_file)
        audio_duration = audio.duration_seconds
        total_duration = total_duration + audio_duration
    print(total_duration)


if __name__ == '__main__':
    audio_path = '/home/synsense/视频/baby_cry_20230306/filter_data'
    cut_data_path = '/home/synsense/视频/baby_cry_20230306/cut_data'

    audio_files = get_file_list(audio_path)
    for audio_file in audio_files:
        cut_audio(audio_file)
    # '''音频总时长'''
    # get_total_duration()




