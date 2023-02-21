import cv2  # opencv库
import os
import time
from time import sleep
from tqdm import tqdm


class Face_processing():
    def __init__(self,image_path,output_path,face_model):
        self.image_path = image_path
        self.output_path = output_path
        self.face_model = face_model


    def Face_recognition(self):
        #获取需要识别的文件全路径(file_path)
        file_list = os.listdir(self.image_path)

        for i in range(len(file_list)):
            file_path = os.path.join(self.image_path,file_list[i])
            print(file_path)

            #判断文件是否存在，如果文件存在，读取文件内图片并识别人脸
            if os.path.isfile(file_path):
                image = cv2.imread(file_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                Faces = self.face_model.detectMultiScale(gray)
                for (x, y, w, h) in Faces:
                    # 1.原始图片；2坐标点；3.矩形宽高 4.颜色值(RGB)；5.线框
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                #显示图片窗口
                cv2.imshow('Face_recognition.png', image)

                #窗口暂停
                cv2.waitKey(0)

                #销毁窗口
                cv2.destroyAllWindows()

                #将识别结果保存至指定路径
                cv2.imwrite(self.output_path + str(time.time()) + '.bmp', image)

            else:
                print('路径不存在')

                # 这里同样的，tqdm就是这个进度条最常用的一个方法
                # 里面存一个可迭代对象
            for i in tqdm(range(10), desc='图片正在识别中',ncols=60):
                time.sleep(0.1)



if __name__ == '__main__':
    image_path = ('/home/synsense/桌面/person.jpg')
    output_path = ('/home/synsense/桌面/')
    os.makedirs(output_path,exist_ok=True)
    face_model = cv2.CascadeClashaarcascade_frontalface_default.xmlsifier('/home/synsense/anaconda3/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    f = Face_processing(image_path,output_path,face_model)
    f.Face_recognition()
