import os
import shutil
from tqdm import tqdm
import time


class move_file_by_name():



    def __init__(self,video_path,txt_path,save_path):
        self.video_path = video_path
        self.save_path = save_path
        self.txt_path = txt_path


    def move_file_by_name(self):
        video_list = (os.listdir(self.video_path))
        with open(self.txt_path, 'r', encoding='utf-8') as f:
                #读取txt内容
                data = f.readlines()
        print(data[0])


        #file_name（视频文件名）
        for i, file_name in enumerate(video_list):
            #获取视频全路径
            video_file = os.path.join(self.video_path,video_list[i])
            #用视频文件名遍历txt文件
            if '，' + file_name.split('.')[0]+'，' in data[0]:
                #将匹配到的视频转移至save_path路径下
                shutil.copy(video_file, self.save_path)
                for a in tqdm(range(1),desc='文件匹配中',ncols=80):
                    time.sleep(0.5)


if __name__ == '__main__':
    video_path = (r'C:\Users\byb\Desktop\down')
    txt_path = (r'C:\Users\byb\Desktop\video.txt')
    save_path = (r'C:\Users\byb\Desktop\save')
    os.makedirs(save_path,exist_ok=True)
    m = move_file_by_name(video_path,txt_path,save_path)
    m.move_file_by_name()
