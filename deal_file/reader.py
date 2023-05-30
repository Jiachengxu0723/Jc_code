import pandas as pd
import os
from tqdm import tqdm
import time

'''
requirement:遍历文件夹下的所有文件并判断是否为excel文件，
如果是则打印出其中“事件类型_时长”sheet中“文件名”和“时长记录”列的内容
parameter：dirPath-需要的文件夹路径，save_path-保存路径
'''
class read_file():
    def __init__(self,dirPath,save_path):
        self.dirPath = dirPath
        self.save_path = save_path


    def Read_excel_specific_lines(self):
        file_list = os.listdir(self.dirPath)
        for i in range(len(file_list)):
            #判断路径下文件是否为excel文件
            file_type = file_list[i].split('.')[-1]
            if file_type in ['xlsx', 'xls']:
                file_path = os.path.join(self.dirPath, file_list[i])
                df = pd.read_excel(file_path, sheet_name='事件类型_时长', usecols=[2,5],dtype ='str',index_col=0)
                print(df)
                #写入文本
                df.to_csv(self.save_path,sep=' ')

        else:print('Ending')

         #打印结果
        # f = open(self.save_path, 'r')
        # for information in f:
        #     print(information)
        # f.close()

if __name__ == '__main__':
    dirPath = (r"/home/mrx/下载/demo")
    save_path = (r'/home/mrx/下载/demo/5')
    r = read_file(dirPath,save_path)
    r.Read_excel_specific_lines()
