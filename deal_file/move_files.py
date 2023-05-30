import os
import shutil

def Get_files_path():
    for model in ['noise','silent']:
        path = '/home/synsense/Downloads/20220705/cut_data/' + model
        file_list = os.listdir(path)
        for i in range(len(file_list)):
            file_path = os.path.join(path,file_list[i])
            return file_path,model

def movefile(file_path,type,new_path):
    files = file_path + '/' + type
    for name in ['huangzirui','liulv']:
        new_file = new_path + name
        os.makedirs()


if __name__ == '__main__':
    for type in ['clap','love','mama','other','papa','twinkle']:
        need_path,model = Get_files_path()
        new_path = '../cut_data' + model
        movefile(need_path,type,new_path)

