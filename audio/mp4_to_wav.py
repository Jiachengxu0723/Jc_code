# 参考： https://github.com/CruelDev69/YouTube-Video-Downloader

from pytube import YouTube 
from colorama import Fore 
from moviepy.editor import * 
import os 
from colorama import Fore 


'''
获取需要的文件列表
    Args:
        directory(string):文件路径
        types(string):需要的文件类型后缀
    Returns:
        file_list(List[str]): 需要的文件列表
'''
def get_file_list(directory, types = ['.mp4'], is_sort = True):
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list

'''
mp4转mp3
    Args:
        mp4_file_path(string):mp4文件列表
        audio_save_path(string):保存路径
    Returns:
        
'''
def mp4_to_wav(mp4_file_path,audio_save_path):
    video_name = mp4_file_path.split('/')[-1].split('.')[0]
    video = VideoFileClip(mp4_file_path)
    audio = video.audio
    if not os.path.exists(audio_save_path):
        os.makedirs(audio_save_path)
    audio.write_audiofile(os.path.join(audio_save_path,f"{video_name}.wav")) # Converting mp4 file to mp3.


def main():
    video_path = './test'
    audio_save_path = './original_data'
    mp4_file_list = get_file_list(video_path)
    for mp4_file in mp4_file_list:
        mp4_to_wav(mp4_file_path = mp4_file, audio_save_path = audio_save_path)

if __name__ == '__main__':
    main()
