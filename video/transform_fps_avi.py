# coding:utf-8
import cv2
import sys,os
import time

#转帧

# def transform_fps(video_path,out_path):
#     save_fps = 25
#
#     for video_file in os.listdir(video_path):
#         #video_file(返回video_path路径下所有文件夹的文件名)
#         print("------****************----",video_file)
#         video_all_file = os.path.join(video_path, video_file)
#         #获取全路径
#         cap = cv2.VideoCapture(video_all_file)
#         #读取video_all_file内的视频
#         hasFrame, frame = cap.read()
#         '''
#         hasFrame判断是否读取成功，返回True或者False。
#         如果读取成功，frame返回每一帧图像
#         '''
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         #fps返回cap video_all_file内视频的cv2.CAP_PROP_FPS
#         print(frame.shape,fps)
#
#
#         frame = roato**()
#
#         out_video = cv2.VideoWriter(os.path.join(out_path, video_file),#os.path.join(out_path, video_file) 要保存的文件路径
#                                     cv2.VideoWriter_fourcc(*'XVID'),#cv2.VideoWriter_fourcc(*'XVID') 指定编码器
#                                     save_fps, #save_fps 要保存的视频帧率
#                                     (frame.shape[1], frame.shape[0]))#(frame.shape[1], frame.shape[0]) 要保存的文件的画面尺寸
#         while hasFrame:
#             # 当视频读取成功时
#             a = out_video.write(frame)
#             #向out_video中写入每一帧图片
#             cv2.imshow("frame", frame)
#             # 展示原图
#             k = cv2.waitKey(1) & 0xFF
#             '''
#             waitKey(1) 中的数字代表等待按键输入之前的无效时间,在这个时间段内按键 ‘q’ 不会被记录
#             在这之后按键才会被记录，并在下一次进入if语段时起作用。也即经过无效时间以后，检测在上一次显示图像的时间段内按键 ‘q’ 有没有被按下
#             若无则跳出if语句段，捕获并显示下一帧图像。
#             '''
#             if k == ord('q'):
#                 break
#
#             hasFrame, frame = cap.read()
#             frame = roato**()
#
#         cap.release()
#         out_video.release()
#         cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     out_path = r"C://Users//byb//Desktop"
#     os.makedirs(out_path, exist_ok=True)ubuntu怎么压缩文件夹
#     video_path =r"C://Users//byb//Desktop//2020-10-20-10-19-14.mp4"
#     transform_fps(video_path,out_path)


class transform():
    def __init__(self,video_path,out_path):
        self.video_path = video_path
        self.out_path = out_path

    def transform_fps(self):
        for video_file in os.listdir(self.video_path):
            # video_file(返回video_path路径下所有文件夹的文件名)
            print("------****************----", video_file)
            video_all_file = os.path.join(video_path, video_file)
            # 获取全路径
            cap = cv2.VideoCapture(video_all_file)
            # 读取video_all_file内的视频
            hasFrame, frame = cap.read()
            fps = cap.get(cv2.CAP_PROP_FPS)
            # fps返回cap video_all_file内视频的cv2.C
            #
            #
            #
            # AP_PROP_FPS
            print(frame.shape, fps)
            frame = roato ** ()

            out_video = cv2.VideoWriter(os.path.join(self.out_path, video_file),
                                        # os.path.join(out_path, video_file) 要保存的文件路径
                                        cv2.VideoWriter_fourcc(*'mp4v'),  # cv2.VideoWriter_fourcc(*'XVID') 指定编码器
                                        save_fps,  # save_fps 要保存的视频帧率
                                        (frame.shape[1], frame.shape[0]))  # (frame.shape[1], frame.shape[0]) 要保存的文件的画面尺寸
            while hasFrame:
                # 当视频读取成功时
                a = out_video.write(frame)
                # 向out_video中写入每一帧图片
                cv2.imshow("frame", frame)
                # 展示原图
                k = cv2.waitKey(1) & 0xFF
                waitKey(1)
                '''
                中的数字代表等待按键输入之前的无效时间, 在这个时间段内按键 ‘q’ 不会被记录
                在这之后按键才会被记录，并在下一次进入if语段时起作用。也即经过无效时间以后，检测在上一次显示图像的时间段内按键 ‘q’ 有没有被按下
                若无则跳出if语句段，捕获并显示下一帧图像。
                '''
                if k == ord('q'):
                    break

                hasFrame, frame = cap.read()
                frame = roato ** ()

if __name__ == '__main__':
    out_path = r"C://Users//byb//Desktop"
    video_path = r"C://Users//byb//Desktop//2020-10-20-10-19-14.mp4"
    fps = 50
    os.makedirs(out_path, exist_ok=True)
    transform_fps(video_path, out_path)
    a = transform(video_path,out_path)
    a.transform_fps()
