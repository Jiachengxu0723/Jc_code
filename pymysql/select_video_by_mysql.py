"""
根据自己设置的条件从数据库里面挑选视频
比如地铁司乘数据库subway_I, 根据event_level的分数来筛选视频，并读取视频路径，把相应的视频挑出来
"""

import mysql_py
import os
import shutil


# 输入待筛选视频路径
data_path = "X:\\嘉成\\cab\\I_data\\20210224_event\\"
# 分数低的视频路径
save_path = "X:\\嘉成\\cab\\I_data\\20210224_event\\low_grade\\"
txt_path = "X:\\嘉成\\cab\\I_data\\20210224_event\\save.txt"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 初始化数据库对象
mysql = mysql_py.Mysql('localhost', 'root', 'byb123456', 'mysql')

# 连接
mysql.connect()

# sql语句
sql = "SELECT video_path, event_level FROM device_eventset WHERE video_path LIKE %s AND event_level < %s GROUP BY " \
"video_path "
# params
params = ['%20210224%', 80]
# 执行
data = mysql.fetchall(sql, params)
# 判断
if data:
    with open(txt_path, 'w+') as f:
        for temp in data:
            print("查询的数据为：", temp)
            f.write(temp[0] + '\t\t' + temp[1] + '\n')

            name = os.path.basename(temp[0])
            input_path = os.path.join(data_path, name)
            if os.path.exists(input_path):
                shutil.move(input_path, save_path)
                print("moving file：", name)
else:
    print('没有数据')


