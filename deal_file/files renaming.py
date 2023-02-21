# -*-coding:utf-8-*-
import os

def File_name_sorting(path):

    dic = {'laugh_b5' : 'video01',
            'laugh_b6' : 'video02',
           'laugh_b7': 'video03',
           'laugh_b8': 'video04',
           'laugh_b9': 'video05',
           'laugh_b10': 'video06',
           'laugh_b11': 'video07',
           'laugh_b12': 'video08',
           'laugh_b13': 'video09',
           'laugh_b14': 'video10',
           'laugh_b15': 'video11',
           'laugh_b16': 'video12',
    }
    files = os.listdir(path)  # 采用listdir来读取所有文件

    for file_name in files:
        fn = file_name.split('.')[0]
        label,num = fn.split('_')[0:2]
        vedio_name = label + '_' + num

        if vedio_name in dic:
            a = file_name.replace(vedio_name, dic[vedio_name])
            old_path = path + os.sep + f'{file_name}'
            new_path = path + os.sep + f'{a}'

            os.rename(old_path, new_path)
            print(f'{file_name} ======> {a}')

def File_name_sorting(path):
    fileList = []
    loss_file_name = []

    files = os.listdir(path)  # 采用listdir来读取所有文件
    for i in files:
        loss_file_name.append(i.strip("laugh_b"))
    loss_file_name.sort(key=lambda x: int(x[:x.find(".")])) # 按照前面的数字字符排序

    for name in loss_file_name:
        fileList.append('laugh_b' + name)

    return fileList

def Rename_by_serial_number(files_name):
    n = 0

    while n < len(files_name):

        #旧路经
        old_path = path + os.sep + files_name[n]

        #填充0
        num = str(n + 1).rjust(2,'0')

        #新文件名
        new_name = 'video'  + num

        #新路径
        new_path = path + os.sep + new_name + ".mp4"

        #改名
        os.rename(old_path, new_path)  # 用os模块中的rename方法对文件改名
        print(old_path, '======>', new_path)

        n +=1

if __name__ == '__main__':
    path = 'data'
    
