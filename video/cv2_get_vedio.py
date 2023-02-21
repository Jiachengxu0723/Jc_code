# coding:utf-8
import cv2
import sys
import time
import argparse 


def parse_args():
    parser = argparse.ArgumentParser(description='cut the video')
    # general
    parser.add_argument('--input',
                        help='input path',
                        type=str,
                        default='')                        
    parser.add_argument('--output',
                        help='out path',
                        type=str,
                        default='')                    
    parser.add_argument('--start',
                        help='input a int',
                        type=int,
                        default=0)      
    parser.add_argument('--end',
                        help='input a int',
                        type=int,
                        default=10)                          
    args = parser.parse_args()
    return args

args = parse_args()
args.path = "F:\\0915站台+车载视频\\II\\20200911\\48.avi"
args.output = "F:\\0915站台+车载视频\\II\\save_0911_I\\"
args.start = 84
args.end = 96
fps = 25
time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
cap = cv2.VideoCapture(args.path)
ret,frame = cap.read()
print(frame.shape)

#此处fourcc的在MAC上有效，如果视频保存为空，那么可以改一下这个参数试试, 也可以是-1
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# 第三个参数则是镜头快慢的，10为正常，小于10为慢镜头
# out = cv2.VideoWriter('./output2'+time+'.avi', fourcc, 8, (frame.shape[1], frame.shape[0]))
out = cv2.VideoWriter( args.output + time + ".mp4", fourcc, 8, (frame.shape[1], frame.shape[0]))
num = 0
while True:
    ret,frame = cap.read()
    num = num + 1
    # if ret == True:
    if num > fps * args.start:
        # frame = cv2.flip(frame, 1)
        a = out.write(frame)
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
    if num > fps * args.end:
        break
cap.release()
out.release()
cv2.destroyAllWindows()




