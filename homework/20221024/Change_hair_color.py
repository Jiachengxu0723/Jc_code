# -*-coding:utf-8-*-
import cv2
import numpy as np
import os

def Traversal_pixel():
    '''
    Function:Change hair color
    '''
    for l in range(87,239):
        for w in range(263,490):
            b, g, r = im[l, w].astype(np.int)
            if b + g + r < 145:
                # print(b,g,r)
                im[l, w] = np.array([b+50, g+70, r+120], dtype=np.uint8)

    cv2.imwrite('resize/non-mainstream.png', im)


if __name__ == '__main__':
    im = cv2.imread('pyy.jpeg')
    if not os.path.exists('resize'):  # os模块判断并创建
        os.mkdir('resize')
    Traversal_pixel()