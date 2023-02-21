import cv2
import os
import time
from datetime import datetime

'''
参数：
path(图片文件夹路径)
outpath（保存路径）

操作说明：
按s或1会将当前展示图片复制到outpath路径
按ESC退出脚本
其他按键跳至下一张

'''
class process_picture():
    def __init__(self,path,outpath):
        self.path = path
        self.outpath = outpath


    def save_picture_from_video(self):
        # 获取文件列表
        video_list = os.listdir(self.path)

        # 批量处理文件
        for i in range(0, len(video_list)):
            print("------*******", str(i), "*********----", video_list[i])
            # 获取 img文件 全路径
            video_file = os.path.join(self.path, video_list[i])

            # 读取视频头
            cap = cv2.VideoCapture(video_file)
            ret, frame = cap.read()
            count = 1
            while ret:
                if count % 8 != 0:
                    count += 1
                    continue
                cv2.imshow(video_list[i], cv2.resize(frame, (1280, 720)))
                k = cv2.waitKey(0)
                if k == ord("s") or k == ord("1"):
                    now_time = datetime.now()
                    cv2.imwrite(self.outpath + video_list[i] , frame)
                    print(now_time.strftime("%Y%m%d_%H%M%S_%f") + " saved")
                if k == ord("q"):
                    break
                if k == 27:
                    exit()
                ret, frame = cap.read()

            cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    # 视频文件路径
    path = ("/home/synsense/下载/dts_annotator_app_20220602")
    # 待保存文件路径
    outpath = ("/home/synsense/桌面/save/")
    # 创建文件夹
    os.makedirs(outpath, exist_ok=True)
    p = process_picture(path, outpath)
    p.save_picture_from_video()

    #now_time.strftime("%Y%m%d_%H%M%S_%f")
