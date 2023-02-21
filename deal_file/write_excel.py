import pandas as pd
import os

def write_excel():
    with open(txt_file, encoding='utf8') as t:
        data = t.readlines()

    line = pd.read_excel(excel_path)
    data0 = line['T1K'].values


    for i in data:
        t1k_need = i.split('\t')[0]
        if t1k_need not in data0:
            print(t1k_need)

def aa(file):
    file_list = os.listdir(file)
    print(file_list)


if __name__ == '__main__':
    txt_file = ('C:\\Users\\byb\\Desktop\\data.txt')
    excel_path = ('C:\\Users\\byb\\Desktop\\西安路局伤损统计（去重）.xlsx')
    w = write_excel()