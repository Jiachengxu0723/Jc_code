import os,json,shutil
'''
# 分析json文件的shapes的列表长度
def json_analysis_shape(json_path):
    data=json.load(open(json_path))
    return len(data['shapes'])

    # 原始文件路径
    json_path = "1_json_file/"
    img_path = "1/"

    # 待保存文件路径
    dest_path1 = "tmp/more_bbox"
    dest_json_path1 = "tmp/more_bbox_json"
    dest_path2 = "tmp/zero_bbox"
    dest_json_path2 = "tmp/zero_bbox_json"

    # 读取文件列表
    jsonlist = os.listdir(json_path)

    # 批量处理文件
    for i in range(len(jsonlist)):
        print("------*******",str(i),"*********----",jsonlist[i])
        # 获取 json 和 img 文件 全路径
        json_file = os.path.join(json_path, jsonlist[i])
        file_prefix = jsonlist[i].split(".")[0]
        img_file = img_path + file_prefix + ".jpg"
        # 分析json文件的shapes的列表长度
        length = json_analysis_shape(json_file)
        # 根据列表长度将json 和 img 文件移动到对应的文件夹
        if length > 18:
            shutil.move(json_file, dest_json_path1)
            shutil.move(img_file, dest_path1)
        elif length < 3:
            shutil.move(json_file, dest_json_path2)
            shutil.move(img_file, dest_path2)
'''


class Json_Analysis():
    def _init_(self,json_path,img_path,outpath):
        self.json_path = json_path
        self.img_path = img_path
        self.dest_path1 = outpath + "/more_bbox"
        self.dest_json_path1 = outpath + "/more_bbox_json"
        self.dest_path2 = outpath + "/zero_bbox"
        self.dest_json_path2 = outpath + "/zero_bbox_json"

        os.mkdir(self.dest_path1)
        os.mkdir(self.dest_json_path1)
        os.mkdir(self.dest_path2)
        os.mkdir(self.dest_json_path2)


    # 分析json文件的shapes的列表长度
    def json_analysis_length(self):
        data=json.load(open(self.json_path))
        return len(data['shapes'])


    def batch_analysis(self):
        jsonlist = os.listdir(self.json_path)
        # 批量处理文件
        for i in range(len(jsonlist)):
            print("------*******", str(i), "*********----", jsonlist[i])
            # 获取 json 和 img 文件 全路径
            json_file = os.path.join(self.json_path, jsonlist[i])
            file_prefix = jsonlist[i].split(".")[0]
            img_file = self.img_path + file_prefix + ".jpg"
            # 分析json文件的shapes的列表长度
            length = self.json_analysis_shape()
            # 根据列表长度将json 和 img 文件移动到对应的文件夹
            if length > 18:
                shutil.move(self.json_file, self.dest_json_path1)
                shutil.move(self.img_file, self.dest_path1)
            elif length < 3:
                shutil.move(self.json_file, self.dest_json_path2)
                shutil.move(self.img_file, self.dest_path2)

if __name__ == "__main__":
    # 原始文件路径
    json_path = "1_json_file/"
    img_path =''
    #对象实例化 "1/"
    outpath = ''
    ar = Json_Analysis(json_path,img_path,outpath)
    ar.batch_analysis()
