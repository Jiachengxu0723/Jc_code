import os,shutil

def file_pc(file_path,json_path):
    file_list = os.listdir(file_path)
    for i in range(len(file_list)):
        all_path = os.path.join(file_path,file_list[i])
        files = file_list[i].split('@')
        print(files)

if __name__ == '__main__':
    #617
    file_path = ('C:\\Users\\byb\Desktop\\tunnel\\TestAccNew23-36-26Num5\\warpCriMask')
    #619
    json_path = ('C:\\Users\\byb\\Desktop\\tunnel\\TestAccNew23-36-26Num5\\warpCri')
    f = file_pc(file_path,json_path)