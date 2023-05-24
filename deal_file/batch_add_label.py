import os
import shutil

def get_txt(path, types='.txt'):
    file_list = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            suffix = os.path.splitext(file)[-1]
            if types == suffix:
                file_list.append(os.path.join(roots, file))
    return sorted(file_list)

def load_data(path):
    data = []
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if line:
                line = line.split()
                data.append(line)
            else:
                break
    return data


def add_label(file_name, data):
    label_data = data.copy()
    for i,item in enumerate(label_data):
        item[2] = f'{file_name}_{str(i+1).zfill(3)}' + '_' + item[2]
    return label_data


def text_save(filename, data):
    file = open(filename,'w')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')
        s = s.replace("', '","\t").replace("'","")+'\n'  
        file.write(s)
    file.close()
    print("保存文件成功") 


def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))  


def main():
    ###*此处路径改为需要处理的文件的路径，然后按执行即可
    lable_path = './txt/train/'
    file_list = get_txt(lable_path)

    for filename in file_list:
        data = load_data(filename)

    # 备份原文件（命名：原标签文件_original）
        file_name = filename.split('/')[-1].split('.')[0]
        copyfile_path = filename.replace(file_name,f'{file_name}_original')
        shutil.copyfile(filename,copyfile_path)

        label_data = add_label(file_name, data)
        print(label_data)

        # 生成新标签文件（与原标签文件同名）
        text_save(filename = filename ,data = label_data)


if __name__ == '__main__':
    main()



