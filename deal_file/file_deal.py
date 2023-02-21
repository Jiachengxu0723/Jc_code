import os,shutil
import re

class file_deal():
    def __init__(self,file_path,save_path):
        self.file_path = file_path
        self.save_path = save_path

    def file_move(self):
        #遍历文件夹
        file_list = os.listdir(self.file_path)
        for i in range(len(file_list)):
            #获取文件夹下的全路径
            cur_path = os.path.join(self.file_path,file_list[i])
           #如果该路径下文件存在
            if os.path.isfile(cur_path):
                # 筛选符合条件的文件
                r = re.findall(r'1-1-0.dll', cur_path)
                #判断文件是否符合条件
                if '1-1-0.dll' in r:
                    print("copying file ...")
                    shutil.copy(cur_path,self.save_path)
                else:
                    print(file_list[i] + '文件不匹配')


if __name__ == '__main__':
    file_path = (r'X:/Navicat Premium 15')
    save_path = (r'C:/Users/Administrator/Desktop/save_path')
    f = file_deal(file_path,save_path)
    f.file_move()


