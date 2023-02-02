# -*-coding:utf-8-*-
import cv2
import os

def enlarge():
    '''
    Function:Double the size of the image
    '''

    shape = im.shape
    img_resize_larger = cv2.resize(im, (shape[0] * 2, shape[1] * 2))
    cv2.imwrite('resize/img_resize_larger.png', img_resize_larger)

def narrow():
    '''
    Function:Reduce the image to a quarter of its original size
    '''

    shape = im.shape
    img_resize_smaller = cv2.resize(im.copy(), (shape[0] // 4, shape[1] // 4))
    cv2.imwrite('resize/img_resize_smaller.png', img_resize_smaller)

def Image_clipping():
    '''
    Function:Cut the middle part
    '''

    Cropping = im[360:720, 360:720]
    cv2.imwrite('resize/Cropping.png', Cropping)

def Picture_conversion():
    '''
    Function:Convert the picture to grayscale
    '''

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('resize/gray.png', gray)

def Draw_Rectangle():
    '''
    Function:Draw Rectangle
    '''

    #参数表示依次为:（图片，长方形框左上角坐标, 长方形框右下角坐标， 字体颜色，字体粗细）
    Rectangle = cv2.rectangle(im.copy(), (456,419), (743,809),(0,165,255),5)
    cv2.imwrite('resize/Draw_Rectangle.png', Rectangle)

def Draw_circle():
    '''
    Function:Draw circle
    '''

    circle = cv2.circle(im.copy(), (611, 622), 148, (255, 255, 0), 4)
    cv2.imwrite('resize/Draw_circle.png', circle)

def Draw_line():
    '''
    Function:Draw line
    '''

    line = cv2.line(im.copy(), (461, 598), (743, 598), (0, 255, 0), 3)
    cv2.imwrite('resize/Draw_line.png', line)

def write_picture():
    '''
    Function:Write in picture
    '''

    write_picture = cv2.putText(im.copy(),'jiachengxu',(461, 598),cv2.FONT_HERSHEY_COMPLEX,1,(0,165,255),2)
    cv2.imwrite('resize/write_picture.png', write_picture)

def show_picture():
    '''
     Function:Show every picture in the folder
    '''
    files = os.listdir(path)
    for pic_files in files:
        #图片路径
        files_name = os.path.join(path, pic_files)
        #图片文件名
        pic_name = pic_files.split('.')[0]

        im = cv2.imread(files_name)
        cv2.imshow(pic_name, im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    enlarge()
    narrow()
    Image_clipping()
    Picture_conversion()
    Draw_Rectangle()
    Draw_circle()
    Draw_line()
    write_picture()
    show_picture()

if __name__ == '__main__':
    im = cv2.imread('lena.png')
    path = ('resize/')
    if not os.path.exists(path):  # os模块判断并创建
        os.mkdir(path)
    main()

