import os,shutil

t1k_path = '//192.168.10.4/public/个人区/w王琦武/use/d/西安路局数据'
txt_path = 'C:\\Users\\byb\\Desktop\\西安局伤损t1k文件名.txt'
save_path = 'C:\\Users\\byb\\Desktop\\save_t1k'
os.makedirs(save_path,exist_ok=True)

with open(txt_path) as t:
    t1k_list = list(set(t.readlines()))
    # i:需要的t1k文件名
    for i in t1k_list:
        i = i.replace('\n', '')
        # print(i)
        for root,dirs,files in os.walk(t1k_path):
            for file in files:
                if i + '.t1k' in file:
                    print (i)
                    continue