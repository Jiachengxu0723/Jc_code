import xlrd
import pandas as pd
import os
import collections


def clear_excel_row():
    df = pd.read_excel(excel_path,usecols=[0])

    df_li = df.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
        ctr = collections.Counter(result)
    print(ctr)


if __name__ == '__main__':
    excel_path =('/home/mrx/下载/.~IMU_zhaojiayin_20220310.xlsx')
    c = clear_excel_row()