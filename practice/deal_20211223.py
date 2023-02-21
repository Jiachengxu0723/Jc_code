import os


'''
读取给出的路径、后缀
返回一个列表包含相应的后缀文件的全路径
'''
def get_file_list(directory, types, is_sort = True):
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list


'''
输入文件路径，返回姓名，光照，位置，类型
'''
def parse_filename(file_list):
    for file_path in file_list:
        filepath, suffix = os.path.splitext(file_path)
        name, light_level, position, label = filepath.split('/')[-4:]
        label = label.split('_')[-1]
        return name, light_level, position, label

def filter_by_attributes(filename, lights = ['l01'], positions=[], names=[], labels=[]):
    name, light_level, position, label = parse_filename(filename)
    if lights:
        if light_level not in lights:
            return False
        else:print('1')

if __name__ == '__main__':
    directory = ('../20211223')
    types = ['.bin']
    file_list = get_file_list(directory, types)
    filename = parse_filename(file_list)




