# -*-coding:utf-8-*-
import cv2
import numpy as np

def hide_numbers():
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            b, g, r = im[i, j].astype(np.int64)
            if b + g + r < 700:
                b = 253
                g = 253
                r = 253
            im[i, j] = np.array([b, g, r], dtype=np.uint8)

    cv2.imwrite('resize/hide.png', im)

if __name__ == '__main__':
    im = cv2.imread('t2.png')
    hide_numbers()