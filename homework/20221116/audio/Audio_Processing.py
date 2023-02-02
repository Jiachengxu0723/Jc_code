# -*-coding:utf-8-*-
import os
from moviepy.editor import *
from pydub import AudioSegment as AS

def mp4_to_mp3(mp4_path:str,file = 'mp4_to_mp3',name = 'Kobe.mp3'):
    video = VideoFileClip(mp4_path)
    audio = video.audio
    if not os.path.exists(file):
        os.makedirs(file)
    mp3_save_path = os.path.join(file,name)
    mp3 = audio.write_audiofile(mp3_save_path)
    return mp3_save_path

def Show_Audio_Properties(mp3:str) -> None:
    song = AS.from_file(mp3, format='mp3')
    print('##音频信息##' + '\n'
        f'---***时长为{len(song)/1000}秒***---' + '\n'
          f'---***声道数为{song.channels}个***---'+ '\n'
          f'---***频率为{song.frame_rate}赫兹***---' + '\n'
          f'---***音量为{song.dBFS}***---' +'\n')
    return song

def audio_clip(mp3,file = 'clip/'):
    song = AS.from_file(mp3, format='mp3')
    if not os.path.exists(file):
        os.makedirs(file)
    mp3_time = int(len(song)/1000)
    for start_time in range(mp3_time + 1):
        sample = song[start_time*1000 : (start_time + 1)*1000]
        save_path = file + str(start_time) + '.wav'
        sample.export(save_path,format = 'wav')
        #print(f'{start_time}.wav保存成功')

def adjust_volume(mp3,file = 'Adjust volume/'):
    song = AS.from_file(mp3, format='mp3')
    if not os.path.exists(file):
        os.makedirs(file)

    increase_song = song + 10
    decrease_volume = song - 10

    decrease_volume.export(file + 'decrease volume.mp3', format='mp3')
    increase_song.export(file + 'increase volume.mp3', format='mp3')

def Audio_connection(file = 'mp4_to_mp3/'):
    for path,[],name in os.walk(file):
        input_music1 = AS.from_file(os.path.join(path,name[1]),format = 'mp3')
        input_music0 = AS.from_file(os.path.join(path, name[0]), format='mp3')

        output_music = input_music1 + input_music0
        output_music.export("Audio_connection.mp3", format="mp3")

def main():
    mp4_path = ('mp4/Kobe.mp4')
    mp3 = mp4_to_mp3(mp4_path)
    Show_Audio_Properties(mp3)
    audio_clip(mp3)
    adjust_volume(mp3)
    Audio_connection()

if __name__ == '__main__':
    main()