import os
import shutil
import csv

def get_file_list(directory, types , is_sort = True):
    r"""
    Get the list of all files names with certain types in a directory
    Args:
        directory(string): the directory that contains all files
        types(List[str]):
        is_sort:
    Returns:
        file_list(List[str]): List of all the required files
    """
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list

def parse_filename(filepath):
    r"""
    Parse the info contained in the file path.
    Args:
        filename(string):file path of the data bin file.
    Returns:
        Parsed attributes from the filename.
    """
    filepath, suffix = os.path.splitext(filepath)
    name, light_level, position, label = filepath.split('/')[-4:]
    label = label.split('_')[-1]
    return name, light_level, position, label

def filter_file_list(file_list,  lights = [], positions=[], names=[], labels=[]):
    r"""
    Filter the file path list by the attributes requirements.
    Args:
        file_list(List[str]): List of the files' file path.
        lights(List[str]): An attribute of file name. Light intensities of data.
        positions(List[str]): An attribute of file name. Camera positions of data.
        names(List[str]): An attribute of file name. Actor names of data.
        labels(List[str]): An attribute of file name. Labels of data.
    Returns:
        file_list[List[str]]: Filtered file path List by the attributes requirements.
    """
    #print(list(filter(lambda x: filter_by_attributes(x, lights, positions, names, labels), file_list)))
    return list(filter(lambda x: filter_by_attributes(x, lights=['l01'],positions=['p04'],labels=['attentive','inattentive']), file_list))

def filter_by_attributes(filename, lights = [], positions=[], names=[], labels=[]):
    r"""
        Check if the file path meets the attributs requirements.
        Args:
            filename(string): file path of the data file.
            lights(List[str]): An attribute of file name. Light intensities of data.
            positions(List[str]): An attribute of file name. Camera positions of data.
            names(List[str]): An attribute of file name. Actor names of data.
            labels(List[str]): An attribute of file name. Labels of data.
        Returns:
            result(bool): Is the file path meets the attributs requirements.
        """
    name, light_level, position, label = parse_filename(filename)
    if lights:
        if light_level not in lights:
            return False
    if positions:
        if position not in positions:
            return False
    if names:
        if name not in names:
            return False
    if labels:
        if label not in labels:
            return False
    return True

def get_the_required_file_path():
    r'''
        Filter the required file paths according to the requirements, and return the list of required file paths

        Returns: List of file paths filtered according to requirements
    '''

    file_list = get_file_list(directory = '20211228' ,types = ['.csv'])
    old_path_list = filter_file_list(file_list,lights=['l01'],positions=['p04'],labels=['attentive','inattentive'])
    return old_path_list

def get_requirement_dictionary():
    r'''
        Output the information that meets the requirements in the form of a dictionary
    @return:dic(Dictionary)
    '''
    dic = {}
    for need_path in get_the_required_file_path():
        date, name, lights , position, label = need_path.split('/')
        with open(need_path) as f:
            reader = csv.reader(f)
            starttime_list = [row[0] for row in reader][1:]

        with open(need_path) as f:
            reader = csv.reader(f)
            endtime_list = [row[1] for row in reader][1:]

        with open(need_path) as f:
            reader = csv.reader(f)
            classification_list = [row[4] for row in reader][1:]

        for (starttime,endtime,class_number) in zip(starttime_list,endtime_list,classification_list):
            times = int(endtime)-int(starttime)
            # lists = [name,times,class_number]
            if class_number == '1':
                continue
            if name in dic:
                if class_number in dic[name]:
                    dic[name][class_number] += times
                else:
                    dic[name][class_number] = times
            else:
                dic[name] = {class_number: times}


    return dic

def llc_writecsv(file, data_dict, filter_mark):
    with open(file, 'w') as f:
        f.write('Name,class0,class2,class3,class4,class5\n')
        for name, data in data_dict.items():
            f.write(name + ',')
            for lable in filter_mark:
                if lable == '5':
                    if lable in data:
                        f.write(str(data[lable])+'\n')
                    else:
                        f.write('0'+'\n')
                else:
                    if lable in data:
                        f.write(str(data[lable])+',')
                    else:
                        f.write('0'+',')

def main():
    '''

    Insert the data in the dictionary into the CSV file as required
    @return:None

    '''
    dics = get_requirement_dictionary()
    row = ['Name', 'class0', 'class2', 'class3', 'class4', 'class5']
    with open("demo.csv", 'a') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(row)

    for names in dics.keys():
        #定义原始列表
        rows = [names, 0, 0, 0, 0, 0, 0]

        for dis_nb,times in dics[names].items():
            for row_nb in row:
                if dis_nb == row_nb.split(',')[-1][-1]:
                    dis_nb = int(dis_nb) +1
                    rows[dis_nb] = times

        #删除列表里的第三列class1
        del rows[2]
        print(rows)
        with open("demo.csv", 'a') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(rows)


'''

作业2：
192.168.8.154/maqitian/media/maqitian/sda1/database/compelete_data/BMW_PoC/data/speck-2b/20211228/
统计每个人(attentive和inattentive)标注信息（只统计L01,P04），计算每个人的标注的attentive时间和inattentive时间。
结果表格形式存储在csv文件中， 共6列：
Name class0 class2 class3 class4 class5
统计每个人(0, 2, 3, 4, 5)各类时间， 时间计算方式：endTime - startTime
提交：计算结果(一个csv)和代码

'''
if __name__ == '__main__':
    main()

