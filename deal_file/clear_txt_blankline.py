import os,tqdm

'''
删除txt文件中的空行/重复的行
txt_file:待处理的txt文件
txt_put:处理后保存路径
read():读取文件内容包括换行符，将内容转为字符串
readline():读取整行包括换行符，转为字符串
readlines():读取文件内容包括换行符，将内容转为列表
'''

def clearblankline():
    with open(txt_file,'r+') as f,open(txt_put,'w+') as new_f:
        '''
        list():转换为列表
        set():去重
        '''
        f_list = list(set(f.readlines()))

        for i in f_list:
            if i == '\n':
                #移除空行
                f_list.remove(i)
            print(i)
         #写入新的文件内
        new_f.writelines(f_list)


if __name__ == '__main__':
    txt_file = 'C:\\Users\\byb\\Desktop\\新建文本文档.txt'
    txt_put = 'C:\\Users\\byb\\Desktop\\西安局伤损t1k文件名.txt'
    c = clearblankline()
