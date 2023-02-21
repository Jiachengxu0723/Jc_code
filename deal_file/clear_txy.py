import os,tqdm

'''
删除txt文件中的空行/重复的行
txt_file:待处理的txt文件
txt_put:处理后保存路径

'''

def clearblankline():
    with open(txt_put, 'r+') as f, open(txt_file, 'w+') as new_f:
        '''
        list():转换为列表
        set():去重
        '''
        f_list = list(set(f.readlines()))
        new_f.writelines(list(set(f_list)))
        print(f_list)


if __name__ == '__main__':
    txt_put = 'C:\\Users\\byb\\Desktop\\西安局伤损t1k文件名.txt'
    txt_file = 'C:\\Users\\byb\\Desktop\\t1k.txt'
    txt = 'C:\\Users\\byb\\Desktop\\data.txt'
    # c = clearblankline()

