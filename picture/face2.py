# -*- coding: utf-8 -*
import cv2
import os
def judge_picture(path):
    pic_list = os.listdir(path)
    for i in range(len(pic_list)):
        if pic_list[i].split('.')[-1] in ['jpg','png','jpge','bmw']:
            pic_path = os.path.join(path,pic_list[i])
            print(pic_path)

def face_detect_function(pictur_path,face_detect):
    gray_img = cv2.cvtColor(pictur_path, cv2.COLOR_BGR2GRAY)
    face = face_detect.detectMultiScale(gray_img)
    for x, y, w, h in face:
        cv2.rectangle(pictur_path, (x, y, w, h), color=(0, 0, 255), thickness=2)  # 能将人脸找出，相机框框
    cv2.imshow('1', pictur_path)


# 读取摄像头
video = cv2.VideoCapture(0)  # 0默认电脑摄像头

# 等待
while True:
    flag, frame = video.read()
    if not flag:
        break
    face_detect_function(frame)
    if ord('q') == cv2.waitKey(1):  # 没有waitkey不显示图片，代码中意思为按q退出
        break
# 释放内存
cv2.destroyAllWindows()
# 释放摄像头
video.release()

if __name__ == '__main__':
    path = ('/home/synsense/桌面/picture')
    # 人脸识别分类器
    face_detect = cv2.CascadeClassifier('/home/synsense/anaconda3/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    picture_path = judge_picture(path)
    face_detect_function(picture_path,face_detect)
