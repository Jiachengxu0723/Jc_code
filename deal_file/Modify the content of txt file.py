# -*-coding:utf-8-*-
import os
import pandas as pd
import shutil
'''
Prefix the third column of the txt file
'''
def load_data(path):
    data = []
    with open(path, 'r') as f:
        while True:
            #读取txt文件每一行
            line = f.readline()
            if line:
                #将每一行以空格切割放进列表
                line = line.split()
                #txt每一行内容列表放进列表
                data.append(line)
            else:
                break
    return data

def add_label(file_name, data,dic):
    label_data = data.copy()
    prefix = dic[file_name.split('_')[-1]]
    suffix = file_name.split('_')[-1]
    for i, item in enumerate(label_data):
        item[2] = f'{prefix}_{suffix}_{str(i + 1).zfill(3)}'
    return label_data

def get_dic(file):
    dic = { }
    for d,ds,fs in os.walk(file):
        for names in fs:
            prefix = names.split('_')[0]
            suffix = names.split('_')[1].split('.')[0]
            dic[suffix] = prefix

    return dic,prefix

def get_file_path(file):
    list = []
    for d,ds,fs in os.walk(file):
        for names in fs:
            file_paths = os.path.join(d,names)
            list.append(file_paths)
    return list

def text_save(filename, data):
    file = open(filename, 'w')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')
        s = s.replace("', '", "\t").replace("'", "") + '\n'
        file.write(s)
    file.close()
    print(f"{filename}保存文件成功")

def change_file(list,dic):
    for file_path in list:
        if os.path.getsize(file_path) > 0:
            # 备份原文件（命名：原标签文件_original）
            file_name = file_path.split('/')[-1].split('.')[0]
            copyfile_path = file_path.replace(file_name, f'{file_name}_original')
            shutil.copyfile(file_path, copyfile_path)
            #txt每一行内容列表
            data = load_data(file_path)

            label_data = add_label(file_name,data,dic)
            # 生成新标签文件（与原标签文件同名）
            text_save(filename=file_path, data=label_data)

def main():
    #需要修改的文件路径
    file = '/home/synsense/下载/1'
    dic,prefix = get_dic(file)
    list = get_file_path(file)
    change_file(list,dic)

if __name__ == '__main__':
    main()