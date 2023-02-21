import os,json,shutil
from base64 import b64encode
import cv2

# usage:   读取labelme格式的json
# input：  json_path             json文件路径
# output： data                  读取的json文件对象
def reference_labelme_json(json_path):
    data = json.load(open(json_path))
    return data

# usage:   将图像转为字符串
# input：  img_path              图像文件路径
# output： data                  base64格式的对象
def img_bytes(img_path):
    with open(img_path, 'rb') as jpg_file:
        byte_content = jpg_file.read()
    # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(byte_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

# 原始文件路径
input_ana_path = "erro\json"
input_img_path = "erro\jpg\\"
# 待保存文件路径
save_json_path = "erro\json_test\\"


# 读取文件列表
jsonlist = os.listdir(input_ana_path)
# print(input_ana_path)
# print(jsonlist)
# 批量处理文件
for i in range(len(jsonlist)):
    print("------*******",str(i),"*********----",jsonlist[i])
    # 获取 json文件 全路径
    json_path = os.path.join(input_ana_path, jsonlist[i])
    # 获取文件名前缀
    file_name_prefix = jsonlist[i].split(".")[0]
    # 读取json信息
    json_data = reference_labelme_json(json_path)
    # 获取 jpg文件 全路径
    img_path = input_img_path + file_name_prefix + ".jpg"
    # 将图像转为字符串
    # img_data = img_bytes(img_path)
    # data_labelme['imageData'] = None
    with open(img_path, 'rb') as jpg_file:
        byte_content = jpg_file.read()
    # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(byte_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode('utf-8')
    # 修改json_data
    json_data['imageData'] = base64_string
    # 另存为json文件
    save_json_file = save_json_path + jsonlist[i]
    json.dump(json_data,open(save_json_file,'w'),indent=4)










