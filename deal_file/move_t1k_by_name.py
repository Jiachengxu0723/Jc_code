import os
import shutil

t1k_file = "C:/Users/Administrator/Desktop/新建文本文档.txt"
search_dir = "//192.168.10.4/public/个人区/w王琦武/use/d/西安路局数据"


with open(t1k_file) as f:
    for t1k_name in f.readlines():
        if t1k_name != "\n":
            all_info = t1k_name.split("DF")
            year = all_info[1][4:6]
            month = int(all_info[1][2:4])
            day = all_info[1][0:2]
            train_num = all_info[0][0:3]
            if train_num == "302":
                if year == "19":
                    path = search_dir + "/2019数据（08711）/" + str(month) + "月/" + str(month) + "月数据/" + str(int(day)) + "/"
                    file = path + t1k_name.strip("\n") + ".t1k"

                elif year == "20":
                    path = search_dir + "/2020数据（08711）/" + str(month) + "月/" + "数据/" + str(
                        int(day)) + "/"
                    file = path + t1k_name.strip("\n") + ".t1k"

            if train_num == "802":
                if year == "19":
                    path = search_dir + "/2019数据（08712）/" + "2019年" + str(month) + "月探伤（80）/" + "数据/" + str(int(day)) + "/"
                    file = path + t1k_name.strip("\n") + ".t1k"

                elif year == "20":
                    path = search_dir + "/2020数据（08712）/" + str(month) + "月802车探伤汇总/" + "数据/" + str(int(day)) + "/"
                    file = path + t1k_name.strip("\n") + ".t1k"

            if train_num == "860":
                path = search_dir + "/2020年08713/数据/2020年" + str(int(month)) + "月/" + str(int(day)) + "/"
                file = path + t1k_name.strip("\n") + ".t1k"

            shutil.copy(file, "C:/Users/Administrator/Desktop/新建文件夹 (2)")
