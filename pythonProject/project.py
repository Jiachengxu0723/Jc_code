from PIL import Image
import numpy as np
import os
from tqdm import tqdm
import time

class process_image():
    def __init__(self,img_path,out_path):
        # self.number = number
        self.img_path = img_path
        self.out_path = out_path

    def change_img(self, num):
        # 加载原图，将图像转化为数组数据
        a = np.asarray(Image.open(self.img_path).convert('L')).astype('float')
        depth = 10.

        # 取图像灰度的梯度值
        grad = np.gradient(a)

        # 取横纵图像梯度值
        grad_x, grad_y = grad
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A

        # 光源的俯视角度转化为弧度值
        vec_el = np.pi / 2.3

        # 光源的方位角度转化为弧度值
        vec_az = np.pi / 4.

        # 光源对x轴的影响
        dx = np.cos(vec_el) * np.cos(vec_az)
        dy = np.cos(vec_el) * np.sin(vec_az)
        dz = np.sin(vec_el)

        # 光源归一化，把梯度转化为灰度
        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)

        # 避免数据越界，将生成的灰度值裁剪至0-255内
        b = b.clip(0, 255)

        # 图像重构
        im = Image.fromarray(b.astype('uint8'))

        # img_list = os.listdir(self.img_path)
        # for i in range(len(img_list)):
        #     img_file = os.path.join(self.img_path, img_list[i])

        for i in tqdm(range(1), desc='图片处理中', ncols=60):
            time.sleep(0.5)
        # im.save(os.path.join(self.out_path,img_file))
        im.save(os.path.join(self.out_path, str(num) + '.jpg'))

    def save_img(self, num):
        self.change_img(num)

if __name__ == '__main__':
    img_path = ('/home/synsense/下载/pic/background.jpg')
    out_path = ('/home/synsense/下载/outpath')
    os.makedirs(out_path,exist_ok=True)
    files = os.listdir(img_path)
    for i, img in enumerate(files):
        image_path = os.path.join(img_path, img)
        p = process_image(image_path, out_path)
        p.save_img(i)
