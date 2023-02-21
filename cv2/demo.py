# -*- coding: utf-8 -*-
import os
import math, cv2
import numpy as np

from cab_action.action_recog import ActionRecog
# from cab_action.caculate_angle import AngleCaculate
from datetime import datetime


def rotate_bound1(image, angle):
    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -angle, 1.0)
    newW = int((h * np.abs(M[0, 1])) + (w * np.abs(M[0, 0])))
    newH = int((h * np.abs(M[0, 0])) + (w * np.abs(M[0, 1])))
    M[0, 2] += (newW - w) / 2
    M[1, 2] += (newH - h) / 2
    return cv2.warpAffine(image, M, (newW, newH))


if __name__ == "__main__":

    t = ActionRecog("config")
    # c = AngleCaculate("config")
    # human_state: sit True        stand False    
    human_state = True
    # path = "test_video/"
    path = "X:\\嘉成\\cab\\I_data\\20210224_event\\low_grade\\"
    error_origin = "erro_img/origin/"
    os.makedirs(error_origin, exist_ok=True)
    error_detect = "erro_img/detect/"
    os.makedirs(error_detect, exist_ok=True)
    pathlist = os.listdir(path)
    for i in range(len(pathlist)):
        print(str(i), "------****************----", pathlist[i])
        t._clear()
        # path_tmp = "20201216_07_20.avi"
        video = os.path.join(path, pathlist[i])
        cap = cv2.VideoCapture(video)
        hasFrame, frame = cap.read()
        num = 1
        while hasFrame:
            # frame = rotate_bound1(frame,90)
            # frame = cv2.resize(frame, (360, 640))
            origin = frame.copy()
            flag, pred = t.action_predict(frame, human_state)
            if flag:
                flag = c.get_angle_list(pred, human_state)
                print(flag, pred["template"])
                # break
            cv2.imshow("result", frame)

            img_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S%f') + '.jpg'
            # print(num,flag)
            k = cv2.waitKey(0)
            if k == ord('1'):
                cv2.imwrite(os.path.join(error_origin, img_name), origin)
                cv2.imwrite(os.path.join(error_detect, img_name), frame)
                print("save img {} success!".format(img_name))
            if k == 27:
                exit()

            hasFrame, frame = cap.read()
            num += 1
