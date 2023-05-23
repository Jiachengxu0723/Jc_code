import os
import shutil



img_path = 'C:\\Users\\byb\\Desktop\\save_xq\\detect'
image_path = 'C:\\Users\\byb\\Desktop\\save_xq\\origin'
out_path = r'C:\\Users\\byb\Desktop\\out_path'
os.makedirs(out_path,exist_ok=True)



img_list = os.listdir(img_path)
for i in range(len(img_list)):
    file_path =(os.path.join(img_path,img_list[i]))
    image_list = os.listdir(image_path)

    n = 0
    for j in range(len(image_list)):
        if img_list[i] == image_list[j]:
            n = n+1
    if n == 0:
        shutil.move(file_path, out_path)



