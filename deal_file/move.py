import os,json,shutil

# 分析json文件的shapes的列表长度
def json_analysis_shape(json_path):
    data=json.load(open(json_path)) 
    return len(data['shapes'])



# 原始文件路径
json_path = "1_json_file//"
img_path = "1//"

# 待保存文件路径
dest_path = "tmp/1"


jsonlist = os.listdir(json_path)

# 批量处理文件
for i in range(1496,len(jsonlist)):
    print("------*******",str(i),"*********----",jsonlist[i])
    # 获取 json 和 img 文件 全路径
    json_file = os.path.join(json_path, jsonlist[i])
    file_prefix = jsonlist[i].split(".")[0]
    img_file = img_path + file_prefix + ".jpg"
    shutil.move(img_file, dest_path)
   