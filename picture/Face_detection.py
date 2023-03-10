import cv2
import os

'''
将文件夹里的所有图片展示，框出里面的人脸
环境：
    python==3.7.0
    oepncv-python==4.7.0.72
    face_detector==1.3.0
操作：
    任意键切换下一张，q键退出
'''
def get_file_list(directory, types, is_sort = True):
    r"""
    Get the list of all files names with certain types in a directory
    Args:
        directory(string): the directory that contains all files
        types(List[str]):
        is_sort:
    Returns:
        file_list(List[str]): List of all the required files
    """
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list

def main():
    for type in ['.jpeg','.jpg','.png','.bmp']:
        picture_list = get_file_list(picture_path,types=type)
        for pic in picture_list:
            img = cv2.imread(pic)  # 读取
            cv2.imshow('image1', img)

            # imgflip = cv2.flip(img,-1)
            img2 = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            cv2.imshow('image2', img2)

            faces = face_detector.detectMultiScale(img2, 1.2, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 1原始图片，2初始坐标点，3矩形宽高4颜色值（RGB)，5线框
            cv2.imshow('image2', img2)  # 显示识别结果image2

            k = cv2.waitKey(0)
            if k == ord("q"):
                #当触发键为q时退出
                break
            else:
                #摧毁窗口
                cv2.destroyAllWindows()


    pass

if __name__ == '__main__':
    #图片文件夹
    picture_path = r'/home/synsense/桌面/picture'
    # 调用分类库（找到自己环境里haarcascade_frontalface_default.xml位置）
    face_detector = cv2.CascadeClassifier(r'/home/synsense/anaconda3/envs/face/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    main()