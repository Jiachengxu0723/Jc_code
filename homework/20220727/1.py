import os
import pprint
import csv



def mymakedirs(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def get_file_list(directory, types = ['.bin'], is_sort = False):
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list


# 写入一行
def write_csv(filepath,data):
    with open(filepath, mode='w', newline='', encoding='utf8') as cf:
        write=csv.writer(cf)
        write.writerow(data)

# 写入多行
def write_csv_rows(filepath,data:list):
    with open(filepath, mode='w', newline='', encoding='utf8') as cf:
        write=csv.writer(cf)
        write.writerows(data)


def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        rows=[row for row in reader]
        return rows


def parse_filename(filepath):
    filepath, suffix = os.path.splitext(filepath)
    name, light_level, position, label = filepath.split('/')[-4:]
    label = label.split('_')[-1]
    return name, light_level, position, label


def filter_by_attributes(filename, lights = ['l01'], positions=[], names=[], labels=[]):
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


def filter_file_list(file_list, lights = ['l01'], positions=[], names=[], labels=[]):
    return list(filter(lambda x: filter_by_attributes(x, lights, positions, names, labels), file_list))


src_file_path = '20211228'
result_filename = src_file_path + '_result_v2.csv'

head_row=['Name','class0','class2','class3','class4','class5']
init_person_data=['Name','0','0','0','0','0']

light_level_mark = ['l01']
position_mark = ['p04']
label_mark = ['attentive','inattentive']


# 初始化一个result csv
write_csv(result_filename,head_row)
# result_content = read_csv(result_filename)
# pprint.pprint(result_content)


file_list = get_file_list(directory = src_file_path, types = ['.csv'], is_sort = True)
# print(file_list)
# print(len(file_list))

file_list = filter_file_list(file_list,lights = light_level_mark, positions=['p04'], labels=['attentive','inattentive'])
# print(file_list)
# print(len(file_list))

for src_file in file_list:
    name, light_level, position, label = parse_filename(src_file)
    result_content = read_csv(result_filename)
    pprint.pprint(result_content)

    if result_content[-1][0] != name:
        result_content.append(init_person_data)
        result_content[-1][0] = name

    person_content = read_csv(src_file)
    # pprint.pprint(person_content)

    for person_data in person_content[1:]:
        startTime = int(person_data[0])
        endTime = int(person_data[1])
        totalTime = endTime - startTime
        classification = person_data[4]

        if classification == '0':
            result_content[-1][1] = int(result_content[-1][1]) + totalTime
        if classification == '2':
            result_content[-1][2] = int(result_content[-1][2]) + totalTime
        if classification == '3':
            result_content[-1][3] = int(result_content[-1][3]) + totalTime
        if classification == '4':
            result_content[-1][4] = int(result_content[-1][4]) + totalTime
        if classification == '5':
            result_content[-1][5] = int(result_content[-1][5]) + totalTime

    #pprint.pprint(result_content)
    write_csv_rows(result_filename,result_content)